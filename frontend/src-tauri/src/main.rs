// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::sync::Mutex;
use tauri::{Manager, RunEvent};

/// Holds the backend child process so we can kill it on exit.
struct BackendProcess(Mutex<Option<tauri::api::process::CommandChild>>);

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // Spawn the Python backend sidecar.
            // In development (debug build) the binary usually doesn't exist yet,
            // so we silently skip if it fails.
            match tauri::api::process::Command::new_sidecar("ai-clipper-backend") {
                Ok(cmd) => match cmd.spawn() {
                    Ok((mut rx, child)) => {
                        app.manage(BackendProcess(Mutex::new(Some(child))));

                        // Forward backend stdout/stderr to the Tauri log
                        tauri::async_runtime::spawn(async move {
                            use tauri::api::process::CommandEvent;
                            while let Some(event) = rx.recv().await {
                                match event {
                                    CommandEvent::Stdout(line) => {
                                        println!("[backend] {line}");
                                    }
                                    CommandEvent::Stderr(line) => {
                                        eprintln!("[backend] {line}");
                                    }
                                    CommandEvent::Terminated(payload) => {
                                        eprintln!(
                                            "[backend] process terminated — code: {:?}",
                                            payload.code
                                        );
                                        break;
                                    }
                                    _ => {}
                                }
                            }
                        });
                    }
                    Err(e) => {
                        eprintln!("[sidecar] failed to spawn backend: {e}");
                    }
                },
                Err(e) => {
                    eprintln!("[sidecar] backend binary not found (dev mode?): {e}");
                }
            }

            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error building tauri application")
        .run(|app_handle, event| {
            // Kill the backend when the last window is closed / app exits
            if let RunEvent::ExitRequested { .. } | RunEvent::Exit = event {
                if let Some(state) = app_handle.try_state::<BackendProcess>() {
                    if let Ok(mut guard) = state.0.lock() {
                        if let Some(mut child) = guard.take() {
                            let _ = child.kill();
                            println!("[sidecar] backend process killed");
                        }
                    }
                }
            }
        });
}

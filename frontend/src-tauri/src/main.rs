// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use tauri::{Manager, RunEvent};

struct BackendProcess(Mutex<Option<Child>>);

fn main() {
    tauri::Builder::default()
        .manage(BackendProcess(Mutex::new(None)))
        .setup(|app| {
            // In dev mode the backend-dist folder doesn't exist — skip.
            #[cfg(not(debug_assertions))]
            {
                let exe_path = app
                    .path_resolver()
                    .resolve_resource("backend-dist/ai-clipper-backend/ai-clipper-backend.exe")
                    .expect("failed to resolve backend resource path");

                match Command::new(&exe_path)
                    .stdout(Stdio::null())
                    .stderr(Stdio::null())
                    .spawn()
                {
                    Ok(child) => {
                        *app.state::<BackendProcess>().0.lock().unwrap() = Some(child);
                        println!("[backend] process started from {:?}", exe_path);
                    }
                    Err(e) => {
                        eprintln!("[backend] failed to spawn {:?}: {e}", exe_path);
                    }
                }
            }
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error building tauri application")
        .run(|app_handle, event| {
            if let RunEvent::ExitRequested { .. } | RunEvent::Exit = event {
                if let Some(state) = app_handle.try_state::<BackendProcess>() {
                    if let Ok(mut guard) = state.0.lock() {
                        if let Some(mut child) = guard.take() {
                            let _ = child.kill();
                            println!("[backend] process killed");
                        }
                    }
                }
            }
        });
}

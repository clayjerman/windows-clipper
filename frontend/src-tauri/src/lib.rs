// lib.rs - Shared library module for AI Clipper

// Use this for shared functions and modules
// Currently, the main application logic is in main.rs

pub fn get_app_version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

pub fn get_app_name() -> &'static str {
    env!("CARGO_PKG_NAME")
}

use std::time::Duration;
use std::thread::sleep;

use monitor;

fn main() {
    simple_monitor();
    detailed_monitor();
}

fn simple_monitor() {
    // Monitor settings
    let width = 60;
    let height = 15;
    let char_1 = Some('#');             // Default is *
    let char_2 = None;                  // Default is -
    let color_1 = Some((68, 131, 73));  // Default is system/terminal color
    let color_2 = Some((40, 50, 66));   // Default is system/terminal color

    // Monitor instance
    let mut monit = monitor::Monitor::new(width, height, char_1, char_2, color_1, color_2);

    // A loop controls the monitor display time
    for _ in 0..width {  // If 'sleep' below is 1 second, then using 60 here is 1 minute in loop
        print!("{esc}[2J{esc}[1;1H", esc = 27 as char); // Clear terminal

        // Utility to emulate real-time value
        let mut bitcoin_value = monitor::ValueEmulator::new(0, height);
        
        // Show monitor
        for monitor_lines in monit.status(bitcoin_value.value()) {
            println!("{}", monitor_lines);
        }
        sleep(Duration::from_millis(100)); // Slow down display
    }
}

fn detailed_monitor() {
    // Settings
    let width = 60;
    let height = 15;
    let char_1 = Some('+');             // Default is *
    let char_2 = Some('-');             // Default is -
    let color_1 = Some((47, 87, 124));  // Default is system/terminal color
    let color_2 = Some((29, 79, 41));   // Default is system/terminal color

    // Instance
    let mut monit = monitor::Monitor::new(width, height, char_1, char_2, color_1, color_2);

    // Show
    for _ in 0..width {
        print!("{esc}[2J{esc}[1;1H", esc = 27 as char); // Clear terminal
        let mut bitcoin_value = monitor::ValueEmulator::new(0, height);

        for (n, m) in monit.status(bitcoin_value.value()).iter().enumerate() {
            println!(" {} {}", m, n + 1);
        }
        println!("  {}", "----|".repeat((width/5) as usize));
        sleep(Duration::from_millis(100));
    }
}

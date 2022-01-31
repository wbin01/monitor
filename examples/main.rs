use std::time::Duration;
use std::thread::sleep;

use monitor;

fn main() {
    simple_monitor();
    detailed_monitor();
}

fn simple_monitor() {
    let mut monit = monitor::Monitor::new();  // Monitor instance

    // A loop controls the monitor display time
    for _ in 0..60 {  // If 'sleep' below is 1 second, then using 60 here is 1 minute in loop
        print!("{esc}[2J{esc}[1;1H", esc = 27 as char); // Clear terminal

        // Utility to emulate real-time value:             (   MIN and MAX values  )
        let mut bitcoin_value = monitor::ValueEmulator::new(0, monit.dimensions().1);
        
        for monitor_lines in monit.build_chart(bitcoin_value.value()) {
            println!("{}", monitor_lines);  // Show monitor
        }
        sleep(Duration::from_millis(100)); // Slow down display (1 second is 1000)
    }
}

fn detailed_monitor() {
    // Instance
    let mut monit = monitor::Monitor::new();
    // Monitor settings
    monit.set_primary_character(Some('*'), Some((47, 87, 124)));
    monit.set_secondary_character(Some('.'), Some((29, 79, 41)));
    monit.set_dimensions(70, 20);  // Width (columns) and height (lines)

    for _ in 0..100 {  // Display time
        print!("{esc}[2J{esc}[1;1H", esc = 27 as char);  // Clear terminal

        // Utility to emulate real-time value:             (   MIN and MAX values  )
        let mut bitcoin_value = monitor::ValueEmulator::new(0, monit.dimensions().1);

        // Show monitor row and right decoration
        for (n, m) in monit.build_chart(bitcoin_value.value()).iter().enumerate() {
            println!(" {} {}", m, n + 1);
        }
        // Bottom decoration
        println!(" {}", "____!____|".repeat(7 as usize));
        let mut n = 10; print!("  "); for _ in 0..7 {print!("        {}", n); n += 10;}

        println!();
        sleep(Duration::from_millis(100));
    }
}

use rand::prelude::*;

#[derive(Debug)]
pub struct Monitor{
    history: Vec<i32>,
    max_value: i32,
    width: i32,
    height: i32,
    primary_character: String,
    secondary_character: String,
    primary_rgb_color: String,
    secondary_rgb_color: String,
}

impl Monitor {
    pub fn new(
        width: i32,
        height: i32,
        primary_character: Option<char>,
        secondary_character: Option<char>,
        primary_rgb_color: Option<(u8, u8, u8)>,
        secondary_rgb_color: Option<(u8, u8, u8)>,
    ) -> Monitor {
        // History
        let mut history = Vec::new();
        for _ in 0..width {
            history.push(0);
        }

        // Max value
        let max_value = height; 

        // Primary character
        let mut primary_char = String::new();
        match primary_character {
            Some(c) => primary_char.push(c),
            None => primary_char.push('*'),
        }

        // Secondary character
        let mut secondary_char = String::new();
        match secondary_character {
            Some(c) => secondary_char.push(c),
            None => secondary_char.push('-'),
        }
        // print!("\x1B[0m"
        // Primary RGB color
        let mut primary_rgb = String::new();
        match primary_rgb_color {
            Some(c) => primary_rgb.push_str(format!("\x1b[38;2;{};{};{}m", c.0, c.1, c.2).as_str()),
            None => primary_rgb.push_str("\x1B[0m"),
        }

        // Secondary RGB color
        let mut secondary_rgb = String::new();
        match secondary_rgb_color {
            Some(c) => secondary_rgb.push_str(format!("\x1b[38;2;{};{};{}m", c.0, c.1, c.2).as_str()),
            None => secondary_rgb.push_str("\x1B[0m"),
        }

        Monitor {
            history,
            max_value,
            width,
            height,
            primary_character: primary_char,
            secondary_character: secondary_char,
            primary_rgb_color: primary_rgb,
            secondary_rgb_color: secondary_rgb,

        }
    }

    pub fn status(&mut self, mut value: i32) -> Vec<String> {
        // Update value for height%. Ex:
        // 1%(max(1000) / height(10)) = 100 | value((500) / 1%(100)) = 5 | 5 = 50%(height(10))
        value = value / (self.max_value / self.height);

        // Create model with historical data and new value 
        let mut model = self.history[1..self.width as usize].to_vec();
        model.push(value);

        // Update history with model value 
        self.history = model.to_vec();

        // Update max value
        if value > self.max_value {
            self.max_value = value;
        }

        // Draw model (String)
        // [0    , 3    , 2    , 5    ]
        // [-----, ***--, **---, *****]
        let mut draw_model: Vec<String> = Vec::new();

        for &value in model.iter() {
            // Draw value
            let mut draw_value = String::new();

            // Update with primary char: 3/5 = *** | 5/5 = *****
            if value > 0 {
                for _ in 0..value {draw_value.push_str(&self.primary_character);}
            }

            // Update with secondary char: 3/5 = ***-- | 0/5 = -----
            if value < self.height {
                let plus = self.height - value;
                for _ in 0..plus {draw_value.push_str(&self.secondary_character);}
            }

            // Update draw model
            draw_model.push(draw_value);
        }
        

        /*  0      3      2      5
         * [-----, ***--, **---, *****]
         *
         * [-      -      -      *    ]
         * [-      -      -      *    ]
         * [-      *      -      *    ]
         * [-      *      *      *    ]
         * [-      *      *      *    ]
         *  0      3      2      5
         */
        let mut list_model: Vec<String> = Vec::new();
        for _ in 0..self.height {
            list_model.push(String::new())
        }

        for n in 0..self.height {
            let mut new_line = String::new();
            
            for line_str in &draw_model {
                let reverse_string: String = line_str.chars().rev().collect();
                
                let char_ = &reverse_string.as_str()[n as usize..(n as usize + 1)];
                let mut new_char = String::new();

                if char_ == self.primary_character {
                    new_char.push_str(
                        format!("{}{}\x1B[0m", self.primary_rgb_color, char_).as_str());
                } else {
                    new_char.push_str(
                        format!("{}{}\x1B[0m", self.secondary_rgb_color, char_).as_str());
                }
                new_line.push_str(new_char.as_str());
            }
            list_model[n as usize].push_str(&new_line);
        }
        
        // Return
        list_model
    }
}

pub struct ValueEmulator {
    min_value: i32,
    max_value: i32,
    reverse: bool,
}

impl ValueEmulator {
    pub fn new (min_value: i32, max_value: i32) -> ValueEmulator{
        ValueEmulator {
            min_value,
            max_value,
            reverse: false,
        }
    }

    pub fn value(&mut self) -> i32 {
        let mut rng = thread_rng();

        let variation = rng.gen_range(4..=5);
        let min = rng.gen_range(self.min_value..=(self.min_value + variation));
        let max = rng.gen_range((self.max_value - variation)..=self.max_value);

        let v = rng.gen_range(min..=max); 

        if self.min_value == self.max_value {
            if !self.reverse{
                self.reverse = true;
            } else {
                self.reverse = false;
            }
        }

        v
    }
}
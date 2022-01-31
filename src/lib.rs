use rand::prelude::*;

#[derive(Debug)]
pub struct Monitor{
    history: Vec<i32>,
    max_value: i32,
    width: i32,
    height: i32,
    primary_character: char,
    new_primary_character: char,
    primary_rgb_color: Option<(u8, u8, u8)>,
    secondary_character: char,
    new_secondary_character: char,
    secondary_rgb_color: Option<(u8, u8, u8)>,
}

impl Monitor {
    pub fn new() -> Monitor {
        // History
        let mut history = Vec::new();
        for _ in 0..60 {
            history.push(0);
        }

        Monitor {
            history,
            max_value: 15,
            width: 60,
            height: 15,
            primary_character: '#',
            new_primary_character: '#',
            primary_rgb_color: None,
            secondary_character: '-',
            new_secondary_character: '-',
            secondary_rgb_color: None,
        }
    }

    pub fn set_primary_character(
            &mut self,
            character: Option<char>,
            rgb_color: Option<(u8, u8, u8)>,
        ) {
        if let Some(c) = character {
            self.new_primary_character = c;
        }
        self.primary_rgb_color = rgb_color;
    }

    pub fn set_secondary_character(
            &mut self,
            character: Option<char>,
            rgb_color: Option<(u8, u8, u8)>,
        ) {
        if let Some(c) = character { 
            self.new_secondary_character = c;
        }
        self.secondary_rgb_color = rgb_color;
    }

    pub fn characters(&self) -> (char, char) {
        (self.primary_character, self.secondary_character)
    }

    pub fn set_dimensions(&mut self, width: i32, height: i32) {
        self.width = width;
        self.height = height;
        self.max_value = height;
        for _ in 0..width {
            self.history.push(0);
        }
    }

    pub fn dimensions(&self) -> (i32, i32) {
        (self.width, self.height)
    }

    pub fn build_chart(&mut self, mut value: i32) -> Vec<String> {
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
                for _ in 0..value {draw_value.push(self.primary_character);}
            }

            // Update with secondary char: 3/5 = ***-- | 0/5 = -----
            if value < self.height {
                let plus = self.height - value;
                for _ in 0..plus {draw_value.push(self.secondary_character);}
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
                // Primary color
                let mut primary_color = String::new();
                if let Some(color) = &self.primary_rgb_color {
                    primary_color = format!(
                        "\x1b[38;2;{};{};{}m", &color.0, &color.1, &color.2);
                }

                // Secondary color
                let mut secondary_color = String::new();
                if let Some(color) = &self.secondary_rgb_color {
                    secondary_color = format!(
                        "\x1b[38;2;{};{};{}m", &color.0, &color.1, &color.2);
                }

                // Character
                let reverse_string: String = line_str.chars().rev().collect();
                let txt = &reverse_string[n as usize..(n as usize + 1)];
                let mut new_char = String::new();

                // Format
                if txt == format!("{}", self.primary_character) {
                    new_char.push_str(
                        format!("{}{}\x1B[0m", primary_color, self.new_primary_character)
                    .as_str());
                } else {
                    new_char.push_str(
                        format!("{}{}\x1B[0m", secondary_color, self.new_secondary_character)
                    .as_str());
                }

                // Update
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
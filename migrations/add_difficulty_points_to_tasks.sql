-- Add difficulty column
ALTER TABLE tasks 
ADD COLUMN difficulty INT DEFAULT 1;

-- Add points column
ALTER TABLE tasks
ADD COLUMN points INT DEFAULT 0;

-- Comment for the new columns
COMMENT ON COLUMN tasks.difficulty IS '1-5 scale for task difficulty';
COMMENT ON COLUMN tasks.points IS 'Points/score value for the task';

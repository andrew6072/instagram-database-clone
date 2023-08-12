CREATE TABLE IF NOT EXISTS App_user
(
  user_id SERIAL PRIMARY KEY,
  first VARCHAR(20) NOT NULL,
  middle VARCHAR(20),
  last VARCHAR(20) NOT NULL,
  username VARCHAR(20) CONSTRAINT valid_len_un CHECK (char_length(username) >= 5) UNIQUE NOT NULL,
  website TEXT CONSTRAINT valid_website CHECK(website LIKE '%.com%'),
  bio TEXT,
  email VARCHAR(80) CONSTRAINT valid_email CHECK(email LIKE '%@%.%') UNIQUE NOT NULL,
  phone VARCHAR(15) CONSTRAINT valid_phone CHECK(phone NOT LIKE '%[^0-9]%') UNIQUE NOT NULL,
  gender VARCHAR(9) CONSTRAINT valid_gender CHECK(gender IN('Male', 'Female', 'Unknown')) NOT NULL DEFAULT 'Unknown',
  password VARCHAR(100) CHECK (char_length(password) >= 8) NOT NULL
);

CREATE TABLE IF NOT EXISTS Post_type
(
  post_type_id SERIAL PRIMARY KEY,
  post_type_name VARCHAR CHECK(post_type_name IN('post', 'story', 'reel')) NOT NULL
);

CREATE TABLE IF NOT EXISTS Post
(
  post_id SERIAL PRIMARY KEY,
  caption TEXT,
  user_id INTEGER REFERENCES App_user ON DELETE CASCADE,
  post_type_id INTEGER REFERENCES Post_type ON DELETE RESTRICT,
  posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS Comment
(
	comment_id SERIAL PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	content TEXT NOT NULL,
	post_id INTEGER REFERENCES Post ON DELETE CASCADE,
	user_id INTEGER REFERENCES App_user ON DELETE CASCADE,
	parent_comment_id INTEGER REFERENCES Comment ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Reaction
(
	reacted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	user_id INTEGER REFERENCES App_user ON DELETE NO ACTION,
	post_id INTEGER REFERENCES Post ON DELETE CASCADE,
	CONSTRAINT no_duplicate_like_from_one_user UNIQUE NULLS NOT DISTINCT (user_id, post_id)
);

CREATE TABLE IF NOT EXISTS Post_media
(
	post_media_id SERIAL PRIMARY KEY,
	media_file_path TEXT NOT NULL,
	longtitude VARCHAR(20) NOT NULL,
	latitude VARCHAR(20) NOT NULL,
	post_id INTEGER REFERENCES Post ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Post_media_User_tag
(
	post_media_id INTEGER REFERENCES Post_media ON DELETE CASCADE,
	user_id INTEGER REFERENCES App_user ON DELETE CASCADE,
	x_coordinate INTEGER NOT NULL,
	y_coordinate INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Filter
(
	filter_id SERIAL PRIMARY KEY,
	filter_name VARCHAR(80) UNIQUE NOT NULL,
	filter_detail text
);

ALTER TABLE Post_media
ADD COLUMN IF NOT EXISTS filter_id INTEGER REFERENCES Filter ON DELETE NO ACTION;

CREATE TABLE IF NOT EXISTS Effect
(
	effect_id SERIAL PRIMARY KEY,
	effect_name VARCHAR(80) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Effect_Post_media 
(
	effect_id INTEGER REFERENCES Effect ON DELETE NO ACTION,
	post_media_id INTEGER REFERENCES Post_media ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Follower
(
	follower_id INTEGER REFERENCES App_user ON DELETE CASCADE,
	followee_id INTEGER REFERENCES App_user ON DELETE CASCADE
);

ALTER TABLE Follower
ADD CONSTRAINT unique_follow UNIQUE NULLS NOT DISTINCT(follower_id, followee_id);
Table users {
  id SERIAL [primary key]
  name VARCHAR(100)
  email VARCHAR(100) [unique]
  password VARCHAR(255)
  created_at TIMESTAMP
}

Table password_resets {
  id SERIAL [primary key]
  user_id INT [ref: > users.id]
  token VARCHAR(255) [unique] 
  created_at TIMESTAMP
}

Table regions {
  id SERIAL [primary key]
  name VARCHAR(100)
}

Table destinations {
  id SERIAL [primary key]
  name VARCHAR(100)
  location VARCHAR(255)
  region_id INT [ref: > regions.id]
  latitude FLOAT
  longitude FLOAT
  description VARCHAR(500)
  image_url VARCHAR(255)
}

Table weather {
  id SERIAL [primary key]
  destination_id INT [ref: > destinations.id]
  temperature FLOAT
  humidity INT
  wind_speed FLOAT
  pressure FLOAT
  wind_direction INT
  weather_condition VARCHAR(50)
  timestamp TIMESTAMP
}

Table recommendations {
  id SERIAL [primary key]
  user_id INT [ref: > users.id]
  destination_id INT [ref: > destinations.id]
  weather_id INT [ref: > weather.id]
  recommended_activity VARCHAR(255)
}

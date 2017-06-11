CREATE CONSTRAINT ON (user:User) ASSERT user.user_id IS UNIQUE;
CREATE CONSTRAINT ON (restaurant:Restaurant) ASSERT restaurant.restaurant_id IS UNIQUE;
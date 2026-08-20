-- Insert NewJeans eras
INSERT INTO eras (name, group_id, month, year)
VALUES 
    ('New Jeans (Debut)', 1, 8, 2022),
    ('Ditto / OMG', 1, 12, 2022), 
    ('Get Up', 1, 7, 2023), 
    ('How Sweet', 1, 5, 2024), 
    ('Supernatural', 1, 6, 2024)
ON CONFLICT (group_id, name) DO NOTHING;

-- Assign NewJeans albums to corresponding eras using spotify_album_id
UPDATE albums a
SET era_id = e.id
FROM (
    VALUES
        ('1HMLpmZAnNyl9pxvOnTovV', 'New Jeans (Debut)'),
        ('7bnqo1fdJU9nSfXQd3bSMe', 'Ditto / OMG'),
        ('45ozep8uHHnj5CCittuyXj', 'Ditto / OMG'),
        ('4N1fROq2oeyLGAlQ1C1j18', 'Get Up'),
        ('5V729UqvhwNOcMejx0m55I', 'Get Up'),
        ('0EhZEM4RRz0yioTgucDhJq', 'How Sweet'),
        ('1FVw30SoC91lq1UZ6N9rwN', 'Supernatural')
) AS v(spotify_album_id, era_name)
JOIN eras e
    ON e.name = v.era_name
    AND e.group_id = 1
WHERE a.spotify_album_id = v.spotify_album_id;

-- Check assignments
SELECT a.id, a.group_id, a.era_id, a.name AS album_name, a.release_date, e.name AS era_name FROM albums a LEFT JOIN eras e on e.id = a.era_id WHERE a.group_id = 1 ORDER BY release_date;

-- Insert LE SSERAFIM eras
INSERT INTO eras (name, group_id, month, year)
VALUES
    ('FEARLESS (Debut)', 3, 5, 2022),
    ('ANTIFRAGILE', 3, 10, 2022),
    ('UNFORGIVEN', 3, 5, 2023),
    ('EASY', 3, 2, 2024),
    ('CRAZY', 3, 8, 2024),
    ('HOT', 3, 3, 2025),
    ('SPAGHETTI', 3, 10, 2025),
    ('PUREFLOW', 3, 5, 2026)
ON CONFLICT (group_id, name) DO NOTHING;

-- Assign LE SSERAFIM albums to corresponding eras
UPDATE albums a
SET era_id = e.id
FROM (
    VALUES
        ('4Mc7WwYH41hgUWeKX25Sot', 'FEARLESS (Debut)'),
        ('3lkxVHwSi9lcHPWzYZ8eSu', 'FEARLESS (Debut)'),
        ('4db6bVyZTtbpZjsCQGyZpl', 'FEARLESS (Debut)'),
        ('4mpznsEPjMQrvD7laIx9UI', 'FEARLESS (Debut)'),

        ('3u0ggfmK0vjuHMNdUbtaa9', 'ANTIFRAGILE'),
        ('6mw2LvoVp9MP0jMv0ZuJla', 'ANTIFRAGILE'),

        ('4Oz7K9DRwwGMN49i4NbVDT', 'UNFORGIVEN'),
        ('1FoKSB8Kc39zc9exXYtNu8', 'UNFORGIVEN'),
        ('3Nu8JF8Jxcn4hVm5wrL7SB', 'UNFORGIVEN'),
        ('4snDidl0spOeD55YeH3HGh', 'UNFORGIVEN'),
        ('28unbkaJvfdbM5zffw9vpc', 'UNFORGIVEN'),
        ('2B11ELMAJKREkxW6Y4fclI', 'UNFORGIVEN'),

        ('1YCj4PZi08G20y2ekGKY0C', 'EASY'),
        ('5jdhMhfZ5gdaQnLsrFgcw4', 'EASY'),
        ('75rFaEWO9nufjSlTcg3wPS', 'EASY'),
        ('4IqfdL14SOkeFN2c5ASmGh', 'EASY'),

        ('538vEfAgLJ6g2I8ubuOlap', 'CRAZY'),
        ('6kAsgfuulBOuyYLytWX7e2', 'CRAZY'),
        ('6bZk9oecizspP2MeHIhKYL', 'CRAZY'),
        ('0hXnUVrrEXKKGUNGfqpdlA', 'CRAZY'),
        ('0Gc4wldZ77F1Mx8tn2HkJO', 'CRAZY'),
        ('2G4myfKwdL4C6sWYj6byB2', 'CRAZY'),
        ('7Bz2elGAw4ZcvLxZyzJofp', 'CRAZY'),
        ('3V9OWu0finGlIhiPkf2XUv', 'CRAZY'),

        ('3lyRrGhXCCMbt4jVO9Wur2', 'HOT'),
        ('5fViZF1K5YS5ELyBCYpVno', 'HOT'),
        ('1f5xm4vrWYjq6SXgWj9Dm5', 'HOT'),
        ('0ki891OZvsxIuBYHn4PPLo', 'HOT'),
        ('0GjZcJIlYoNHn442Tf0hNT', 'HOT'),
        ('5p6KkE9SBq8MJPD0EFrNAF', 'HOT'),
        ('0XBFnNqFyAKPJoo3ikzvBe', 'HOT'),

        ('2yUrwTLHDWBrW74Ewuw6RX', 'SPAGHETTI'),
        ('0ElLaBBHmkoS0UL2nmM0YA', 'SPAGHETTI'),

        ('7vQRIpYlfMRCGU9GUx8Fko', 'PUREFLOW'),
        ('47nSJKWgIL0t2zFQCUemaL', 'PUREFLOW'),
        ('2jujmpcT8jcjKiyQzLfh2l', 'PUREFLOW'),
        ('0wti1ZxzH9QwP4J4DJaYMq', 'PUREFLOW'),
        ('742CzMg7nWRm2ClrwEgUGu', 'PUREFLOW'),
        ('75hJprktMQH4gn3lhgtemt', 'PUREFLOW'),
        ('7EG3id1xZ0TeLEVybwzDJ0', 'PUREFLOW'),
        ('7E3e5DA6v13J0hL9mPPwR1', 'PUREFLOW')
) AS v(spotify_album_id, era_name)
JOIN eras e
    ON e.name = v.era_name
    AND e.group_id = 3
WHERE a.spotify_album_id = v.spotify_album_id;

-- Check assignments
SELECT a.id, a.group_id, a.era_id, a.name AS album_name, a.release_date, e.name AS era_name FROM albums a LEFT JOIN eras e on e.id = a.era_id WHERE a.group_id = 3 ORDER BY release_date;

-- Insert ILLIT eras
INSERT INTO eras (name, group_id, month, year)
VALUES
    ('Super Real Me (Debut)', 2, 3, 2024),
    ('I''LL LIKE YOU', 2, 10, 2024),
    ('bomb', 2, 6, 2025),
    ('Toki Yo Tomare', 2, 8, 2025),
    ('NOT CUTE ANYMORE', 2, 11, 2025),
    ('MAMIHLAPINATAPAI', 2, 4, 2026)
ON CONFLICT (group_id, name) DO NOTHING;

-- Assign ILLIT albums to corresponding eras
UPDATE albums a
SET era_id = e.id
FROM (
    VALUES
        ('6irebIc6UO8fN0jl4UlzBS', 'Super Real Me (Debut)'),
        ('11jrnA9QDULaGEJ5sPYEoe', 'Super Real Me (Debut)'),
        ('3N7bSRtr9USCEbSYOfSlEJ', 'Super Real Me (Debut)'),

        ('7CBwpeVQ27cWwyEYjByVH1', 'I''LL LIKE YOU'),
        ('1rQZODajANwqhegpEuCYk4', 'I''LL LIKE YOU'),
        ('5dbwsmGyS60oSMkh2CwzoD', 'I''LL LIKE YOU'),

        ('6tcKWEXikmRDB9KufEHvLp', 'bomb'),
        ('0ywumXNrnINKlPDkli38ni', 'bomb'),
        ('0XKtGPLlJMTOP4DmhRpOwg', 'bomb'),

        ('34XoGWHnpRwZZieuoUN6sP', 'Toki Yo Tomare'),
        ('4ILU2mLs1ZNAXGmqIynhuO', 'Toki Yo Tomare'),
        ('775URHH5FqYCkzxswNR7nZ', 'Toki Yo Tomare'),

        ('6wKHLrZczZAhDVsMEG4JXt', 'NOT CUTE ANYMORE'),
        ('2T9oFW02VSegOMJvB5782U', 'NOT CUTE ANYMORE'),

        ('5VIt2dA2StboE900mllWdJ', 'MAMIHLAPINATAPAI')
) AS v(spotify_album_id, era_name)
JOIN eras e
    ON e.name = v.era_name
    AND e.group_id = 2
WHERE a.spotify_album_id = v.spotify_album_id;

-- Check assignments
SELECT a.id, a.group_id, a.era_id, a.name AS album_name, a.release_date, e.name AS era_name FROM albums a LEFT JOIN eras e on e.id = a.era_id WHERE a.group_id = 2 ORDER BY release_date;
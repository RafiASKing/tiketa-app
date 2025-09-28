"""Sample movie data used to seed the database during app start-up."""

from datetime import date


SAMPLE_MOVIES = [
    {
        "title": "Spirited Away",
        "description": "A young girl navigates a spirit world to free her parents from a mysterious curse.",
        "poster_path": "/posters/spirited_away.jpg",
        "backdrop_path": "/backdrops/spirited_away.jpg",
        "release_date": date(2001, 7, 20),
        "genre_ids": [16, 10751, 12]
    },
    {
        "title": "Your Name",
        "description": "Two teens mysteriously swap bodies and race against time to change their intertwined fate.",
        "poster_path": "/posters/your_name.jpg",
        "backdrop_path": "/backdrops/your_name.jpg",
        "release_date": date(2016, 8, 26),
        "genre_ids": [16, 18, 10749]
    },
    {
        "title": "Akira",
        "description": "Neo-Tokyo faces chaos when a teen biker unlocks a government secret with psychic power.",
        "poster_path": "/posters/akira.jpg",
        "backdrop_path": "/backdrops/akira.jpg",
        "release_date": date(1988, 7, 16),
        "genre_ids": [16, 28, 878]
    },
    {
        "title": "Ghost in the Shell",
        "description": "A cyborg detective hunts a hacker in a world where the line between human and machine blurs.",
        "poster_path": "/posters/ghost_in_the_shell.jpg",
        "backdrop_path": "/backdrops/ghost_in_the_shell.jpg",
        "release_date": date(1995, 11, 18),
        "genre_ids": [16, 878, 53]
    },
    {
        "title": "Attack on Titan: Chronicle",
        "description": "Humanity battles towering titans in a desperate fight for survival within massive walls.",
        "poster_path": "/posters/aot_chronicle.jpg",
        "backdrop_path": "/backdrops/aot_chronicle.jpg",
        "release_date": date(2020, 7, 17),
        "genre_ids": [16, 28, 12]
    },
    {
        "title": "Mobile Suit Gundam SEED Freedom",
        "description": "Kira Yamato and friends confront a renewed threat to peace in the Orb Union.",
        "poster_path": "/posters/gundam_seed_freedom.jpg",
        "backdrop_path": "/backdrops/gundam_seed_freedom.jpg",
        "release_date": date(2024, 1, 26),
        "genre_ids": [16, 28, 878]
    },
    {
        "title": "Interstellar",
        "description": "Explorers travel through a wormhole searching for a new home as Earth becomes uninhabitable.",
        "poster_path": "/posters/interstellar.jpg",
        "backdrop_path": "/backdrops/interstellar.jpg",
        "release_date": date(2014, 11, 7),
        "genre_ids": [12, 18, 878]
    },
    {
        "title": "Blade Runner 2049",
        "description": "A replicant blade runner uncovers a secret that could shatter the balance between humans and androids.",
        "poster_path": "/posters/blade_runner_2049.jpg",
        "backdrop_path": "/backdrops/blade_runner_2049.jpg",
        "release_date": date(2017, 10, 6),
        "genre_ids": [18, 878, 53]
    },
    {
        "title": "Dune",
        "description": "A gifted heir fights to protect his people and spice-rich desert world from ruthless houses.",
        "poster_path": "/posters/dune.jpg",
        "backdrop_path": "/backdrops/dune.jpg",
        "release_date": date(2021, 10, 22),
        "genre_ids": [12, 18, 878]
    },
    {
        "title": "The Matrix",
        "description": "A hacker discovers reality is a simulation and joins a rebellion to free humanity.",
        "poster_path": "/posters/the_matrix.jpg",
        "backdrop_path": "/backdrops/the_matrix.jpg",
        "release_date": date(1999, 3, 31),
        "genre_ids": [28, 878]
    },
    {
        "title": "Star Wars: A New Hope",
        "description": "A farm boy becomes a hero in the Rebel Alliance's mission to destroy the Death Star.",
        "poster_path": "/posters/star_wars_a_new_hope.jpg",
        "backdrop_path": "/backdrops/star_wars_a_new_hope.jpg",
        "release_date": date(1977, 5, 25),
        "genre_ids": [12, 28, 878]
    },
    {
        "title": "Mad Max: Fury Road",
        "description": "Warrior Imperator Furiosa joins forces with Max to escape a tyrant in a post-apocalyptic desert.",
        "poster_path": "/posters/mad_max_fury_road.jpg",
        "backdrop_path": "/backdrops/mad_max_fury_road.jpg",
        "release_date": date(2015, 5, 15),
        "genre_ids": [28, 12, 878]
    },
    {
        "title": "Everything Everywhere All at Once",
        "description": "An overwhelmed mother taps into multiverse versions of herself to save existence.",
        "poster_path": "/posters/everything_everywhere.jpg",
        "backdrop_path": "/backdrops/everything_everywhere.jpg",
        "release_date": date(2022, 3, 25),
        "genre_ids": [28, 35, 878]
    },
    {
        "title": "Black Panther",
        "description": "T'Challa returns to Wakanda to defend his throne and share his nation's power with the world.",
        "poster_path": "/posters/black_panther.jpg",
        "backdrop_path": "/backdrops/black_panther.jpg",
        "release_date": date(2018, 2, 16),
        "genre_ids": [28, 12, 878]
    },
    {
        "title": "The Dark Knight",
        "description": "Batman faces the Joker in a battle for Gotham's soul.",
        "poster_path": "/posters/the_dark_knight.jpg",
        "backdrop_path": "/backdrops/the_dark_knight.jpg",
        "release_date": date(2008, 7, 18),
        "genre_ids": [28, 80, 18]
    },
    {
        "title": "Inception",
        "description": "A thief enters people's dreams to implant an idea that could change the world.",
        "poster_path": "/posters/inception.jpg",
        "backdrop_path": "/backdrops/inception.jpg",
        "release_date": date(2010, 7, 16),
        "genre_ids": [28, 878, 53]
    },
    {
        "title": "Pulp Fiction",
        "description": "Interwoven crime stories collide in Tarantino's darkly comic classic.",
        "poster_path": "/posters/pulp_fiction.jpg",
        "backdrop_path": "/backdrops/pulp_fiction.jpg",
        "release_date": date(1994, 10, 14),
        "genre_ids": [80, 53]
    },
    {
        "title": "Parasite",
        "description": "A poor family infiltrates a wealthy household, triggering unexpected consequences.",
        "poster_path": "/posters/parasite.jpg",
        "backdrop_path": "/backdrops/parasite.jpg",
        "release_date": date(2019, 5, 30),
        "genre_ids": [35, 18, 53]
    },
    {
        "title": "The Lord of the Rings: The Fellowship of the Ring",
        "description": "A hobbit and his allies embark on a quest to destroy a ring of ultimate evil.",
        "poster_path": "/posters/lotr_fellowship.jpg",
        "backdrop_path": "/backdrops/lotr_fellowship.jpg",
        "release_date": date(2001, 12, 19),
        "genre_ids": [12, 14, 28]
    },
    {
        "title": "Coco",
        "description": "A young musician journeys to the Land of the Dead to uncover his family's legacy.",
        "poster_path": "/posters/coco.jpg",
        "backdrop_path": "/backdrops/coco.jpg",
        "release_date": date(2017, 10, 20),
        "genre_ids": [16, 12, 10751]
    },
    {
        "title": "La La Land",
        "description": "An aspiring actress and a jazz pianist fall in love while chasing their Hollywood dreams.",
        "poster_path": "/posters/la_la_land.jpg",
        "backdrop_path": "/backdrops/la_la_land.jpg",
        "release_date": date(2016, 12, 9),
        "genre_ids": [35, 18, 10749]
    }
]

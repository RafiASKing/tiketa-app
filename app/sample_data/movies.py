"""Sample movie data used to seed the database during app start-up."""

from datetime import date

SAMPLE_MOVIES = [
    {
        "studio_number": 1,
        "title": "Spirited Away",
        "description": "A young girl navigates a spirit world to free her parents from a mysterious curse.",
        "poster_path": "https://images.weserv.nl/?url=theposterdb.com/api/assets/111928/view",
        "backdrop_path": "/backdrops/spirited_away.jpg",
        "release_date": date(2001, 7, 20),
        "trailer_youtube_id": "GAp2_0JJskk",
        "genre_ids": [16, 10751, 12],
        "genres": ["Animation", "Fantasy", "Family"]
    },
    {
        "studio_number": 2,
        "title": "Your Name",
        "description": "Two teens mysteriously swap bodies and race against time to change their intertwined fate. A very romantic and memorable movie by Makoto Shinkai.",
        "poster_path": "https://images.weserv.nl/?url=theposterdb.com/api/assets/90914/view",
        "backdrop_path": "/backdrops/your_name.jpg",
        "release_date": date(2016, 8, 26),
        "trailer_youtube_id": "k4xGqY5IDBE",
        "genre_ids": [16, 18, 10749],
        "genres": ["Animation", "Drama", "Romance"]
    },
    {
        "studio_number": 3,
        "title": "Akira",
        "description": "Neo-Tokyo faces chaos when a teen biker unlocks a government secret with psychic power.",
        "poster_path": "https://image.tmdb.org/t/p/original/6pG3nVF7uWvFPCrNRBGwZqFhoQT.jpg",
        "backdrop_path": "/backdrops/akira.jpg",
        "release_date": date(1988, 7, 16),
        "trailer_youtube_id": "nA8KmHC2Z-g",
        "genre_ids": [16, 28, 878],
        "genres": ["Animation", "Action", "Science Fiction"]
    },
    {
        "studio_number": 4,
        "title": "Ghost in the Shell",
        "description": "A cyborg detective hunts a hacker in a world where the line between human and machine blurs.",
        "poster_path": "https://images.weserv.nl/?url=theposterdb.com/api/assets/98465/view",
        "backdrop_path": "/backdrops/ghost_in_the_shell.jpg",
        "release_date": date(1995, 11, 18),
        "trailer_youtube_id": "rU6Matng9MU",
        "genre_ids": [16, 878, 53],
        "genres": ["Animation", "Science Fiction", "Thriller"]
    },
    {
        "studio_number": 5,
        "title": "Attack on Titan: Requiem",
        "description": "Alternate ending of Attack on Titan, or is it?",
        "poster_path": "https://image.tmdb.org/t/p/original/l1IrdT6ou25RfUHUwBiZ4sCcVFk.jpg",
        "backdrop_path": "/backdrops/aot_chronicle.jpg",
        "release_date": date(2020, 7, 17),
        "trailer_youtube_id": "E7WytLM2KvY",
        "genre_ids": [16, 28, 12],
        "genres": ["Animation", "Action", "Adventure"]
    },
    {
        "studio_number": 6,
        "title": "Mobile Suit Gundam SEED Freedom",
        "description": "In C.E.75, the fighting still continues. There are independence movements, and aggression by Blue Cosmos... In order to calm the situation, a global peace monitoring agency called COMPASS is established, with Lacus as its first president. As members of COMPASS, Kira and his comrades intervene into various regional battles. Then a newly established nation called Foundation proposes a joint operation against a Blue Cosmos stronghold.",
        "poster_path": "https://image.tmdb.org/t/p/original/1EBnttleJaKnWWyyEqfiSn76ZjT.jpg",
        "backdrop_path": "/backdrops/gundam_seed_freedom.jpg",
        "release_date": date(2024, 1, 26),
        "trailer_youtube_id": "Gsj6ToFTGgc",
        "genre_ids": [16, 28, 878],
        "genres": ["Animation", "Action", "Science Fiction"]
    },
    {
        "studio_number": 7,
        "title": "Interstellar",
        "description": "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.",
        "poster_path": "https://image.tmdb.org/t/p/original/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "backdrop_path": "/backdrops/interstellar.jpg",
        "release_date": date(2014, 11, 7),
        "trailer_youtube_id": "zSWdZVtXT7E",
        "genre_ids": [12, 18, 878],
        "genres": ["Adventure", "Drama", "Science Fiction"]
    },
    {
        "studio_number": 8,
        "title": "Blade Runner 2049",
        "description": "A replicant blade runner uncovers a secret that could shatter the balance between humans and androids.",
        "poster_path": "https://image.tmdb.org/t/p/original/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",
        "backdrop_path": "/backdrops/blade_runner_2049.jpg",
        "release_date": date(2017, 10, 6),
        "trailer_youtube_id": "gCcx85zbxz4",
        "genre_ids": [18, 878, 53],
        "genres": ["Drama", "Science Fiction", "Thriller"]
    },
    {
        "studio_number": 9,
        "title": "Dune: Part Two",
        "description": "ABSOLUTE CINEMA, THE BEST FILM EVER MADE, ~ Rafi",
        "poster_path": "https://image.tmdb.org/t/p/original/6izwz7rsy95ARzTR3poZ8H6c5pp.jpg",
        "backdrop_path": "/backdrops/dune.jpg",
        "release_date": date(2021, 10, 22),
        "trailer_youtube_id": "U2Qp5pL3ovA",
        "genre_ids": [12, 18, 878],
        "genres": ["Adventure", "Drama", "Science Fiction"]
    },
    {
        "studio_number": 10,
        "title": "The Matrix",
        "description": "A hacker discovers reality is a simulation and joins a rebellion to free humanity.",
        "poster_path": "https://image.tmdb.org/t/p/original/p96dm7sCMn4VYAStA6siNz30G1r.jpg",
        "backdrop_path": "/backdrops/the_matrix.jpg",
        "release_date": date(1999, 3, 31),
        "trailer_youtube_id": "vKQi3bBA1y8",
        "genre_ids": [28, 878],
        "genres": ["Action", "Science Fiction"]
    },
    {
        "studio_number": 11,
        "title": "Star Wars: A New Hope",
        "description": "A farm boy becomes a hero in the Rebel Alliance's mission to destroy the Death Star.",
        "poster_path": "https://image.tmdb.org/t/p/original/2Cm0oygiJpk7tzboSvX8F86v8PW.jpg",
        "backdrop_path": "/backdrops/star_wars_a_new_hope.jpg",
        "release_date": date(1977, 5, 25),
        "trailer_youtube_id": "vZ734NWnAHA",
        "genre_ids": [12, 28, 878],
        "genres": ["Adventure", "Action", "Science Fiction"]
    },
    {
        "studio_number": 12,
        "title": "Mad Max: Fury Road",
        "description": "Warrior Imperator Furiosa joins forces with Max to escape a tyrant in a post-apocalyptic desert.",
        "poster_path": "https://image.tmdb.org/t/p/original/hA2ple9q4qnwxp3hKVNhroipsir.jpg",
        "backdrop_path": "/backdrops/mad_max_fury_road.jpg",
        "release_date": date(2015, 5, 15),
        "trailer_youtube_id": "hEJnMQG9ev8",
        "genre_ids": [28, 12, 878],
        "genres": ["Action", "Adventure", "Science Fiction"]
    },
    {
        "studio_number": 13,
        "title": "Everything Everywhere All at Once",
        "description": "An overwhelmed mother taps into multiverse versions of herself to save existence.",
        "poster_path": "https://image.tmdb.org/t/p/original/u68AjlvlutfEIcpmbYpKcdi09ut.jpg",
        "backdrop_path": "/backdrops/everything_everywhere.jpg",
        "release_date": date(2022, 3, 25),
        "trailer_youtube_id": "wxN1T1uxQ2g",
        "genre_ids": [28, 35, 878],
        "genres": ["Action", "Comedy", "Science Fiction"]
    },
    {
        "studio_number": 14,
        "title": "Black Panther",
        "description": "T'Challa returns to Wakanda to defend his throne and share his nation's power with the world.",
        "poster_path": "https://image.tmdb.org/t/p/original/uxzzxijgPIY7slzFvMotPv8wjKA.jpg",
        "backdrop_path": "/backdrops/black_panther.jpg",
        "release_date": date(2018, 2, 16),
        "trailer_youtube_id": "xjDjIWPwcPU",
        "genre_ids": [28, 12, 878],
        "genres": ["Action", "Adventure", "Science Fiction"]
    },
    {
        "studio_number": 15,
        "title": "The Dark Knight",
        "description": "Batman faces the Joker in a battle for Gotham's soul.",
        "poster_path": "https://image.tmdb.org/t/p/original/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "backdrop_path": "/backdrops/the_dark_knight.jpg",
        "release_date": date(2008, 7, 18),
        "trailer_youtube_id": "EXeTwQWrcwY",
        "genre_ids": [28, 80, 18],
        "genres": ["Action", "Crime", "Drama"]
    },
    {
        "studio_number": 16,
        "title": "Inception",
        "description": "A thief enters people's dreams to implant an idea that could change the world.",
        "poster_path": "https://image.tmdb.org/t/p/original/ljsZTbVsrQSqZgWeep2B1QiDKuh.jpg",
        "backdrop_path": "/backdrops/inception.jpg",
        "release_date": date(2010, 7, 16),
        "trailer_youtube_id": "YoHD9XEInc0",
        "genre_ids": [28, 878, 53],
        "genres": ["Action", "Science Fiction", "Thriller"]
    },
    {
        "studio_number": 17,
        "title": "Pulp Fiction",
        "description": "Interwoven crime stories collide in Tarantino's darkly comic classic.",
        "poster_path": "https://image.tmdb.org/t/p/original/vQWk5YBFWF4bZaofAbv0tShwBvQ.jpg",
        "backdrop_path": "/backdrops/pulp_fiction.jpg",
        "release_date": date(1994, 10, 14),
        "trailer_youtube_id": "s7EdQ4FqbhY",
        "genre_ids": [80, 53],
        "genres": ["Crime", "Thriller"]
    },
    {
        "studio_number": 18,
        "title": "Parasite",
        "description": "A poor family infiltrates a wealthy household, triggering unexpected consequences.",
        "poster_path": "https://image.tmdb.org/t/p/original/nMF2GX9SriEMbixRvI23KZwCs0U.jpg",
        "backdrop_path": "/backdrops/parasite.jpg",
        "release_date": date(2019, 5, 30),
        "trailer_youtube_id": "SEUXfv87Wpk",
        "genre_ids": [35, 18, 53],
        "genres": ["Comedy", "Drama", "Thriller"]
    },
    {
        "studio_number": 19,
        "title": "The Lord of the Rings: The Fellowship of the Ring",
        "description": "A hobbit and his allies embark on a quest to destroy a ring of ultimate evil.",
        "poster_path": "https://image.tmdb.org/t/p/original/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
        "backdrop_path": "/backdrops/lotr_fellowship.jpg",
        "release_date": date(2001, 12, 19),
        "trailer_youtube_id": "V75dMMIW2B4",
        "genre_ids": [12, 14, 28],
        "genres": ["Adventure", "Fantasy", "Action"]
    },
    {
        "studio_number": 20,
        "title": "Coco",
        "description": "Iori's Favorite movie",
        "poster_path": "https://image.tmdb.org/t/p/original/6Ryitt95xrO8KXuqRGm1fUuNwqF.jpg",
        "backdrop_path": "/backdrops/coco.jpg",
        "release_date": date(2017, 10, 20),
        "trailer_youtube_id": "Rvr68u6k5sI",
        "genre_ids": [16, 12, 10751],
        "genres": ["Animation", "Adventure", "Family"]
    },
    {
        "studio_number": 21,
        "title": "La La Land",
        "description": "The only Good romance movie according to Locos Tacos Hermanos",
        "poster_path": "https://image.tmdb.org/t/p/original/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg",
        "backdrop_path": "/backdrops/la_la_land.jpg",
        "release_date": date(2016, 12, 9),
        "trailer_youtube_id": "0pdqf4P9MB8",
        "genre_ids": [35, 18, 10749],
        "genres": ["Comedy", "Drama", "Romance"]
    }
]

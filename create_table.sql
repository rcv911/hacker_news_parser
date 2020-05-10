BEGIN;

CREATE TABLE public.posts (
    id SERIAL NOT NULL,
    title VARCHAR(1024),
    url VARCHAR(1024),
    created VARCHAR(100),
    PRIMARY KEY (id)
);

COMMIT;

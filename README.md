# Welcome to FaSPP Bender

**FaSPP** is a boilerplate project using:

- **Fa**stAPI 🐍
- **S**QLAlchemy 🗃️
- **P**ostgreSQL 🐘
- **P**ydantic ✅

# About FaSPP Bender

The project originally started as a _conceptual guide_ in upgrading a legacy API project that was originally written in _Django/DRF/PostgreSQL_ stack. In order to support our team's move to an enhanced version of this API using the latest package versions and to get away with growing problems in the old project due to poor package dependency management, I wrote a specialized Python project that still supports the existing major operations and legacy databases of the old Django API project.<br/><br/>

Among the capabilities that were introduced was the employment of `JWT authentication` (a requirement to support specific use cases e.g. to support the `NextAuth` integration for Next.js-based frontend clients) while still supporting a more secured authentication mechanism using `Knox` which was originally used in the Django project. By doing this, our team's new FasPP-based API project (dubbed `Arko`) is able to provide support to knox-based authentication requirements of the old Django project, thereby allowing both APIs to run together and in parallel. This capability ensures that new features written in Arko can be authorized _(as required)_ to and from the Django API until such time that all legacy operations have been migrated to FaSPP-based one.

From being an internal tool, FaSPP Bender now becomes a straightforward boilerplate which is designed for teams that are switching to FasAPI from practically any legacy Python-based API projects.

# Database Management

## Modeling

Database models are primarily supported using [SQLAlchemy](https://docs.sqlalchemy.org/en/20/).

## Migration

Since the project was originally used to support legacy system and databases, it currently does not support migration due to how our legacy databases were written in such a highly-customized and complex manner at that time. However, it does not limit the ability to introduce such mechanism. For example, one can fork the project and introduce Alembic (or any other migration tool) so long as their use case requires.

The project originally powers anyone that requires a backward flow of creating SQLAlchemy models from a legacy database, or if there is anyone that prefers defining the database directly followed by model definition 😅.

## PostgreSQL

The project is originally designed for [PostgreSQL](https://www.postgresql.org/docs/), although anyone may refactor their forked version to support their desired databases.

## Base Database

Initially, the project has `public.auth_user`, `public.knox_authtoken`, `system.api_client`, and `common.tag` tables to support the boilerplate functionality. Feel free to scale or modify your forked version as you require.<br/><br/>

You may explore the existing SQLAlchemy databases (found under `models` folder of each `module` in this project) to replicate the database tables, or you may also execute the following queries below:

### public.auth_user
```
CREATE TABLE public.auth_user (
	id serial4 NOT NULL,
	"password" varchar(128) NOT NULL,
	last_login timestamptz NULL,
	is_superuser bool NOT NULL,
	username varchar(150) NOT NULL,
	first_name varchar(30) NOT NULL,
	last_name varchar(150) NOT NULL,
	email varchar(254) NOT NULL,
	is_staff bool NOT NULL,
	is_active bool NOT NULL,
	date_joined timestamptz NOT NULL,
	CONSTRAINT auth_user_email_key UNIQUE (email),
	CONSTRAINT auth_user_pkey PRIMARY KEY (id),
	CONSTRAINT auth_user_username_key UNIQUE (username)
);
```

### public.knox_authtoken
```
CREATE TABLE public.knox_authtoken (
	digest varchar(128) NOT NULL,
	salt varchar(16) NOT NULL,
	created timestamptz NOT NULL,
	user_id int4 NOT NULL,
	expiry timestamptz NULL,
	token_key varchar(8) NOT NULL,
	CONSTRAINT knox_authtoken_pkey PRIMARY KEY (digest),
	CONSTRAINT knox_authtoken_salt_key UNIQUE (salt),
	CONSTRAINT knox_authtoken_user_id_e5a5d899_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE INDEX knox_authtoken_digest_188c7e77_like ON public.knox_authtoken USING btree (digest varchar_pattern_ops);
CREATE INDEX knox_authtoken_salt_3d9f48ac_like ON public.knox_authtoken USING btree (salt varchar_pattern_ops);
CREATE INDEX knox_authtoken_token_key_8f4f7d47 ON public.knox_authtoken USING btree (token_key);
CREATE INDEX knox_authtoken_token_key_8f4f7d47_like ON public.knox_authtoken USING btree (token_key varchar_pattern_ops);
CREATE INDEX knox_authtoken_user_id_e5a5d899 ON public.knox_authtoken USING btree (user_id);
```

### system.api_client
```
CREATE TABLE "system".api_client (
	id bigserial NOT NULL,
	"name" varchar(100) NOT NULL,
	"token" varchar(32) NOT NULL,
	alias varchar(200) NOT NULL,
	is_active bool NOT NULL DEFAULT false,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NULL,
	CONSTRAINT api_client_pk PRIMARY KEY (id)
);
```

### common.tag
```
CREATE TABLE common.tag (
	id bigserial NOT NULL,
	"name" varchar(50) NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NULL,
	created_by_id int4 NOT NULL,
	updated_by_id int4 NULL,
	CONSTRAINT tag_pkey PRIMARY KEY (id),
	CONSTRAINT tag_created_by_id_6de6b378_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT tag_updated_by_id_174c3678_fk_auth_user_id FOREIGN KEY (updated_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED
);
```

# Authentication

## JSON Web Token (JWT)

API clients, especially web-based apps, are highly-supported with [JWT](https://jwt.io/introduction) authentication. Using the JWT method, one is given `access` and `refresh` tokens which are used to authorize endpoints and request new token, respectively.

## Knox

Knox is a more secured authentication method which is also supported in this project. While the Knox integration is essentially based on secure pseudo-random number generator (CSPRNG) provided by the OS, this capability provide a secure, unpredictable token that cannot be _fingerprintable_ or _reproducible_. This method, however, does not currently support token renewal (refresh), but a forked version may choose to implement as needed.<br/><br/>

The implementation introduced in this project is basically a customized version based on the one implemented in [Django-Rest-Knox](https://jazzband.github.io/django-rest-knox/?utm_source=chatgpt.com).

## API Client Credential

API Client credential authorization using any string token is also supported for protected endpoints intended to be accessed by specific API clients registered in `system.api_clients` database table. If your app requires such use case, you may take advantage of this functionality. There is no policy or restriction as to the method of generating or verifying the token - as long as the provided token matches what has been registered in the database then it authorizes the request.<br/><br/>

Definition of any policy is up to anyone to implement in their respective forked version, although the base functionality has already been provided. When authorizing a request that requires or supports a API Client token, such token must be provided through `X-Client-Key` request header, but of course you may change this header name as you require.<br/><br/>

You may check the **[GET] Tag** documentation on Swagger (`/v1/docs/#/Tag/load_tags_v1_common_tags__get`) for sample implementation of a request supporting API Client token.

# Structured Modeling & Serialization

Data modeling/typing and serialization are primarily supported using [Pydantic](https://docs.pydantic.dev/latest/api/base_model/).

# Build & Deployment

The project implements containerization using [Docker](https://docs.docker.com/) for simpler, faster build, test, and deploy operations.

# Running Development

`uvicorn` is employed in this project, and a development environment may be ran like so:
```
uvicorn app.main:app
```
This runs the app on `localhost:8000` by default, but the `--port` command may be supplied if a specific port number is required. Additionally, `--reload` may be supplied to watch code changes. For example:
```
uvicorn app.main:app --port=8001 --reload
```

# API Documentation
## Swagger
Swagger documentation is accessible through `/v1/docs/`. API can be tested directly here on Swagger so you don't need to separately do them on API clients (e.g. Postman, Hoppscotch, etc.)
## Redocly
Documentation is also accessible using Redocly, through `/v1/redoc/`. Although, unlike Swagger, the Redocly version does not provide ability to execute endpoints for testing.
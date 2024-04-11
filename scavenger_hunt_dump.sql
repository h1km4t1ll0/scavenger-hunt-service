--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1
-- Dumped by pg_dump version 15.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: results; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.results (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    team_id uuid NOT NULL,
    task_id uuid NOT NULL,
    amount integer
);


ALTER TABLE public.results OWNER TO postgres;

--
-- Name: solved_quiz; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.solved_quiz (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    team_id uuid NOT NULL,
    points integer NOT NULL
);


ALTER TABLE public.solved_quiz OWNER TO postgres;

--
-- Name: solved_tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.solved_tasks (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    task_id uuid NOT NULL,
    team_id uuid NOT NULL
);


ALTER TABLE public.solved_tasks OWNER TO postgres;

--
-- Name: task; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text,
    description text,
    type text NOT NULL,
    image text,
    flag text,
    with_manager boolean NOT NULL,
    manager_id bigint,
    amount integer,
    usage integer
);


ALTER TABLE public.task OWNER TO postgres;

--
-- Name: team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    token text NOT NULL,
    amount integer,
    name text,
    member_number integer,
    visible boolean
);


ALTER TABLE public.team OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    chat_id bigint NOT NULL,
    url text,
    username text,
    full_name text,
    role text NOT NULL,
    team_id uuid
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_chat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_chat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_chat_id_seq OWNER TO postgres;

--
-- Name: user_chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_chat_id_seq OWNED BY public."user".chat_id;


--
-- Name: user chat_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN chat_id SET DEFAULT nextval('public.user_chat_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
fa336814cae8
\.


--
-- Data for Name: results; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.results (id, team_id, task_id, amount) FROM stdin;
50958dc0-eb12-43ff-8a79-e28de038a2c1	adc27406-3c20-44e1-99da-92e1e132e40d	1653f3b9-56d9-48ff-ae50-eb2f0970433a	1
\.


--
-- Data for Name: solved_quiz; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.solved_quiz (id, team_id, points) FROM stdin;
\.


--
-- Data for Name: solved_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.solved_tasks (id, task_id, team_id) FROM stdin;
98f72e07-c11d-4cde-aa15-f3609e3dc7e3	1653f3b9-56d9-48ff-ae50-eb2f0970433a	adc27406-3c20-44e1-99da-92e1e132e40d
\.


--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task (id, name, description, type, image, flag, with_manager, manager_id, amount, usage) FROM stdin;
949fc983-28fb-41d4-9407-42b8ed8acc62	Poster creation	Design a poster as instructed by Charintseva Maria Viktorovna - room 1156	offline	\N	1_offline	f	\N	10	1000
715a1f98-f1b5-4064-9bd4-3190a14d44e5	Storytelling	Create an original story to score points.\nYou can complete this task with Lankina Daria Sergeevna – room 1155	offline	\N	2_offline	f	\N	10	1000
bf2d7728-a759-4d01-ae10-4b4ecbecb359	Outdoor communication challenge	Make a video interviewing a passer-by concerning the history of Academgorodok (3-5 minutes)	offline	\N	3_offline	t	\N	10	1000
1ce9608b-6c8a-473a-b6e1-f247285a1bc3	Lights! Camera! Action!	Create a video up to 1 minute long showcasing "my way to NSU"	offline	\N	4_online	t	\N	10	1000
d77a4c1b-63c3-4588-8339-77b2a9b96c31	Group photo	Take a photo of your entire team where everyone is doing a unique type of physical activity)))	offline	\N	5_online	t	\N	5	1000
b87a62a7-0fe2-4bf5-8bd4-fc8fc29a9247	Find an object	Find an object starting with H letter and bring it to Anna Grigorievna Serikova – room 1154. Also there you can find some riddles to get additional points.	offline	\N	6_offline	f	\N	3	1000
719e79f5-723a-4150-8178-7e023f352292	Dune	Make a photo and send it to us	cosplay	dune.jpg	1_cosplay	t	\N	3	1000
dd496e22-f4a2-4082-a51b-5087b2673d70	Barbie	Make a photo and send it to us	cosplay	barbie.jpg	2_cosplay	t	\N	3	1000
bb6ce5d8-b1e5-49fe-8be0-0ed45eb0bd42	Mr. Robot	Make a photo and send it to us	cosplay	mr_robot.jpg	3_cosplay	t	\N	3	1000
5f814559-837c-4bbb-b2d8-639b7fff0ddd	Oppenheimer	Make a photo and send it to us	cosplay	oppenheimer.jpg	4_cosplay	t	\N	3	1000
09addafc-0210-40b1-bca6-cca617262d66	One Punch man	Make a photo and send it to us	cosplay	anime.jpg	5_cosplay	t	\N	3	1000
69574dc5-4feb-4738-92eb-7058afcb01a9	Ninja turtles	Make a photo and send it to us	cosplay	turtles.jpg	6_cosplay	t	\N	3	1000
86074128-83ce-4ece-8142-46909c98a58e	secret1	find me	secret	\N	HELLO_WASSUP_WASSUP_WASSUUUP	f	\N	1	1000
1e1c3080-76fe-408b-94c5-50cebf9f3eca	secret2	find me	secret	\N	INTEGRATING_IN_YOUR_MIND	f	\N	1	1000
cfe125d3-c5ea-4c26-8f23-d5eacb80f551	secret3	find me	secret	\N	CUTE_CAPYBARA_WITH_HUNTER_KNIFE	f	\N	1	1000
1fbdaf69-1382-42bb-8fa8-0b5cdee7cb52	secret4	find me	secret	\N	PREPARE_FOR_EXAM_IN_TWO_DAYS	f	\N	1	1000
1207f5db-89b6-4a83-8ba0-b525d3c30a6b	secret5	find me	secret	\N	JOIN_THE_FOURIER_SERIES	f	\N	1	1000
07fa6b31-63e7-4bfb-b8d4-1d42c68b73b3	secret6	find me	secret	\N	IAM_A_JAVA_MACHINE	f	\N	1	1000
5c761a09-9980-43af-b929-02ca186cf85a	secret7	find me	secret	\N	EIGHT_ANALOG_INPUT_PINS	f	\N	1	1000
4e532c3f-003c-4fab-ba49-fa5ef01ffd1e	secret8	find me	secret	\N	WE_ARE_TIRED_HELP_US	f	\N	1	1000
ba2c774a-0c66-467b-8854-4c320df5a9c8	secret9	find me	secret	\N	MATH_ROOMS_INSTEAD_OF_MUSHROOMS	f	\N	1	1000
af1e15a9-d8dc-434a-b10e-6956b3d5fbb5	secret10	find me	secret	\N	CAPYBARA_ALTER_EGO_WEIGHT	f	\N	1	1000
d8c5f78f-0a81-4b75-ad48-8c3a0c60bae6	secret11	find me	secret	\N	BUFFER_OVERFLOW_PUNISHMENT	f	\N	1	1000
4537164c-4c2c-4abb-b413-7b7b9f178bea	secret12	find me	secret	\N	KERNEL_ADDRESS_SANITIZER	f	\N	1	1000
ae0155e3-b7b2-4e9c-a64a-bea97a78f0ed	secret13	find me	secret	\N	RAP_INSTEAD_OF_DIFFERENTIALS	f	\N	1	1000
eabc1bbd-2362-48e3-8517-d04ae5d8326a	secret14	find me	secret	\N	RELAX_YOUR_RIBS	f	\N	1	1000
da25a048-9f04-4a66-aa4d-012267febc42	secret15	find me	secret	\N	RM_RF_YOUR_BRAIN_AND_CHILL	f	\N	1	1000
1c5f0ad1-a307-4c4d-a00d-f4ff0660690a	secret16	find me	secret	\N	YOU_ARE_A_CUTE_KITTEN	f	\N	1	1000
2f4983a3-d3b0-44f7-95db-0ee7c2280df5	secret17	easter egg	secret	\N	JOKING_INSTEAD_OF_WORKING	f	\N	1	1000
387b192a-8c46-46a8-b040-6d11fd269ee1	Ryan Gosling - I'm just Ken	Summarize a song in a creative way\nhttps://youtu.be/RIHExGaxfPE?si=SE__2NBOMrgXfyCz	song summarization	\N	1_song	t	\N	2	1000
035c7bcb-6954-4b6d-b074-dd373c279414	Imagine Dragons - It's ok	Summarize a song in a creative way\nhttps://youtu.be/W_yRODJ6kfc?si=YDN0gNCRuc35nGYi	song summarization	\N	2_song	t	\N	2	1000
b2829365-3c3e-493a-a3f5-c2eae8eeee91	NF - HOPE	Summarize a song in a creative way\nhttps://youtu.be/xvFcp16NWjo?si=IwkR61DzA6KUF1bM	song summarization	\N	3_song	t	\N	2	1000
5e47eb94-ec5b-4bf7-89be-9b28ba824510	Steve Angello - Dopamine	Summarize a song in a creative way\nhttps://youtu.be/PF8vAhRMUhQ?si=3FG1rX-uApPVREmr	song summarization	\N	4_song	t	\N	2	1000
2f539811-01cc-4eb1-850e-e864c34f59ac	Linkin Park - In the end	Summarize a song in a creative way\nhttps://youtu.be/eVTXPUF4Oz4?si=SkIcWbsDV9eGjl9c	song summarization	\N	5_song	t	\N	2	1000
59faff6a-0554-4a2f-956b-a73641ca944a	My Chemical Romance - Welcome To The Black Parade	Summarize a song in a creative way\nhttps://youtu.be/RRKJiM9Njr8?si=hL5zOZ8JZLK53vUb	song summarization	\N	6_song	t	\N	2	1000
7a5ce243-cb45-4fc3-90bd-bc7bba39f936	Scorpions - Wind Of Change	Summarize a song in a creative way\nhttps://youtu.be/n4RjJKxsamQ?si=t4QMl8SkfJiZi8PC	song summarization	\N	7_song	t	\N	2	1000
cf59fc6a-2908-44c0-9440-d97d2c4f8974	Kodaline - Follow Your Fire	Summarize a song in a creative way\nhttps://youtu.be/i9wBXC3aZ_I?si=lV1U8h5zBrl2GTB9	song summarization	\N	8_song	t	\N	2	1000
bbb6794f-4154-4962-a490-6cf0dd887c90	Eminem - Mockingbird	Summarize a song in a creative way\nhttps://youtu.be/S9bCLPwzSC0?si=kYecHmNoRgzcAqe5	song summarization	\N	9_song	t	\N	2	1000
dcf9cb17-d60b-4237-8060-8e2f51ac7287	Daft Punk - Around The World	Summarize a song in a creative way\nhttps://youtu.be/K0HSD_i2DvA?si=gPEOQbz-q_h0Hle3	song summarization	\N	10_song	t	\N	2	1000
f7a09022-080d-45de-a505-93dc4b5eb9b9	hat (easy)	Take a photo with the item that rhymes the word 'hat'. Please, send the photo AND the name of the item.	rhymes	\N	rt_1	t	\N	1	1
4d6f7656-5c7e-43b4-a0f2-cb2270b851f8	book (easy)	Take a photo with the item that rhymes the word 'book'. Please, send the photo AND the name of the item.	rhymes	\N	rt_2	t	\N	1	1
9612fe48-d576-4f5b-8448-6ac8988da37d	chair (easy)	Take a photo with the item that rhymes the word 'chair'. Please, send the photo AND the name of the item.	rhymes	\N	rt_3	t	\N	1	1
cc6a6003-a213-4007-8836-c5beb26335ef	door (easy)	Take a photo with the item that rhymes the word 'door'. Please, send the photo AND the name of the item.	rhymes	\N	rt_4	t	\N	1	1
fbcc3789-a9bf-4eaf-a716-d97e84e5c2cf	pen (easy)	Take a photo with the item that rhymes the word 'pen'. Please, send the photo AND the name of the item.	rhymes	\N	rt_5	t	\N	1	1
e51a3fb7-6f05-4041-b9a1-ea926f3652c0	clock (easy)	Take a photo with the item that rhymes the word 'clock'. Please, send the photo AND the name of the item.	rhymes	\N	rt_6	t	\N	1	1
ae5f468c-a9cd-462a-9d41-0e39ab9dcbb9	tree (easy)	Take a photo with the item that rhymes the word 'tree'. Please, send the photo AND the name of the item.	rhymes	\N	rt_7	t	\N	1	1
8a413a84-1d9d-44da-b7f3-245b65cd874c	shoe (easy)	Take a photo with the item that rhymes the word 'shoe'. Please, send the photo AND the name of the item.	rhymes	\N	rt_8	t	\N	1	1
ac8448ce-bb28-4b1f-93ee-e5bc7839aef4	cup (easy)	Take a photo with the item that rhymes the word 'cup'. Please, send the photo AND the name of the item.	rhymes	\N	rt_9	t	\N	1	1
20f2ebaf-34f9-4ed7-b2eb-39af27682658	lamp (easy)	Take a photo with the item that rhymes the word 'lamp'. Please, send the photo AND the name of the item.	rhymes	\N	rt_10	t	\N	1	1
1653f3b9-56d9-48ff-ae50-eb2f0970433a	secret18	easter egg	secret	\N	THIS_IS_A_FLAG	f	\N	1	999
af822568-a67b-4f11-8583-b752d9a1be64	bag (easy)	Take a photo with the item that rhymes the word 'bag'. Please, send the photo AND the name of the item.	rhymes	\N	rt_11	t	\N	1	1
04d8fb8a-964d-4185-91f8-e72639dc26a7	key (easy)	Take a photo with the item that rhymes the word 'key'. Please, send the photo AND the name of the item.	rhymes	\N	rt_12	t	\N	1	1
29e031bd-3652-4437-b623-c429f8dfa012	phone (easy)	Take a photo with the item that rhymes the word 'phone'. Please, send the photo AND the name of the item.	rhymes	\N	rt_13	t	\N	1	1
a43b837e-19a3-48fa-a3e4-f5f1740ac726	glass (easy)	Take a photo with the item that rhymes the word 'glass'. Please, send the photo AND the name of the item.	rhymes	\N	rt_14	t	\N	1	1
2096105a-4973-40c7-827c-5078414e2b8e	plate (easy)	Take a photo with the item that rhymes the word 'plate'. Please, send the photo AND the name of the item.	rhymes	\N	rt_15	t	\N	1	1
cf24c035-92be-4149-aa10-cc5e4b69d375	window (medium)	Take a photo with the item that rhymes the word 'window'. Please, send the photo AND the name of the item.	rhymes	\N	rt_16	t	\N	3	1
4994592e-2fd5-4e83-af9a-272e742e9cb9	table (medium)	Take a photo with the item that rhymes the word 'table'. Please, send the photo AND the name of the item.	rhymes	\N	rt_17	t	\N	3	1
e41aada1-a160-4c88-9208-3e53e43c71c9	mirror (medium)	Take a photo with the item that rhymes the word 'mirror'. Please, send the photo AND the name of the item.	rhymes	\N	rt_18	t	\N	3	1
93fac1de-18c3-4c76-a274-3644cb22345d	picture (medium)	Take a photo with the item that rhymes the word 'picture'. Please, send the photo AND the name of the item.	rhymes	\N	rt_19	t	\N	3	1
1fb8b995-e552-495f-b413-9e0b604b1463	flower (medium)	Take a photo with the item that rhymes the word 'flower'. Please, send the photo AND the name of the item.	rhymes	\N	rt_20	t	\N	3	1
b8e49257-5366-45aa-95f7-a572d0aedfb1	basket (medium)	Take a photo with the item that rhymes the word 'basket'. Please, send the photo AND the name of the item.	rhymes	\N	rt_21	t	\N	3	1
0088e94b-26da-4201-993a-e8d321b30c4c	pillow (medium)	Take a photo with the item that rhymes the word 'pillow'. Please, send the photo AND the name of the item.	rhymes	\N	rt_22	t	\N	3	1
0fe7f131-b943-470a-ba36-d1e47b9c82ab	candle (medium)	Take a photo with the item that rhymes the word 'candle'. Please, send the photo AND the name of the item.	rhymes	\N	rt_23	t	\N	3	1
c6f9bd6c-dc9d-4053-9aa5-20242e163f30	marker (medium)	Take a photo with the item that rhymes the word 'marker'. Please, send the photo AND the name of the item.	rhymes	\N	rt_24	t	\N	3	1
274f516c-8e2b-4268-9f1d-ee8d64454d9a	bottle (medium)	Take a photo with the item that rhymes the word 'bottle'. Please, send the photo AND the name of the item.	rhymes	\N	rt_25	t	\N	3	1
6690032b-cc81-4b48-ab43-8192998e1e63	chandlier (hard)	Take a photo with the item that rhymes the word 'chandlier'. Please, send the photo AND the name of the item.	rhymes	\N	rt_26	t	\N	5	1
e8c2a7cd-66fb-4e8f-929c-187773a003d3	sculpture (hard)	Take a photo with the item that rhymes the word 'sculpture'. Please, send the photo AND the name of the item.	rhymes	\N	rt_27	t	\N	5	1
04c5ff87-3e28-4d06-9deb-da0fc799253c	fountain (hard)	Take a photo with the item that rhymes the word 'fountain'. Please, send the photo AND the name of the item.	rhymes	\N	rt_28	t	\N	5	1
7f179698-8919-4a76-b512-5e85d061ef09	tapestry (hard)	Take a photo with the item that rhymes the word 'tapestry'. Please, send the photo AND the name of the item.	rhymes	\N	rt_29	t	\N	5	1
260b7380-04f9-4b62-990a-8e1ea1c61c87	laboratory (hard)	Take a photo with the item that rhymes the word 'laboratory'. Please, send the photo AND the name of the item.	rhymes	\N	rt_30	t	\N	5	1
5d56b1b3-48c1-43b4-ad02-866a18646d01	Invent a word	Create a new word and explain it	online	\N	1_online	t	\N	3	1000
60500eb2-79cb-4064-a059-86c354b38d74	Create a meme	Create your own meme and send us.\nIt can be a meme about your group, faculty, or... We don't know, just use your imagination and humor	online	\N	2_online	t	\N	6	1000
\.


--
-- Data for Name: team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.team (id, token, amount, name, member_number, visible) FROM stdin;
8e137189-1e56-4b23-9061-0210b3b61b24	POSTAL_THOMISTIC_WOODY_BIRTHRIGHT	0	22201	0	t
95961f8d-a56d-47a2-a9c3-3e2b09a1e63c	VULPINE_WASHBURN_CONDENSE_SYNAPTIC	0	22202	0	t
6f97aecb-e86d-4ae7-b9c9-837a0afbd8e2	UMBER_VICARIOUS_DENT_SALTBUSH	0	22203	0	t
b17ccf20-d1dc-455c-9ae2-57e1ca66abc6	AEROSOL_JIFFY_WILLOUGHBY_LOQUAT	0	22204	0	t
d9cb4f02-dbda-4c40-b68c-e04002f07933	SHIP_CHANCERY_NARCOSIS_WIZARD	0	22205	0	t
57a6c240-809a-4ff3-bcc4-6f775a99b70a	ECHO_SKYSCRAPE_GLEAN_STAIR	0	22206	0	t
125b2db7-3fb4-4a7c-80d0-939c3ce5051b	TAMMANY_GRIM_WINY_SQUEAK	0	22207	0	t
0f6a9dab-b6d8-4898-95a2-44b4be19a0f4	BENGAL_MOLLUSK_HERB_DIRECT	0	22208	0	t
e3215d63-98ed-45d2-b5a7-87a837a770b3	POSSESSOR_LIVEN_INFIRMARY_NAUGHTY	0	22209	0	t
486350e8-97cc-4dc9-a6d8-21ab9efbf392	STROM_CARTESIAN_INSUFFICIENT_SATURABLE	0	22210	0	t
24a147d9-b208-4b4e-a235-ec58258abb43	LICHEN_ADVERB_SPLUTTER_PASSAIC	0	22214	0	t
d87a0477-1ef4-4697-9423-823abd880554	MERGE_HERBIVOROUS_SELFRIDGE_LIMBO	0	22215	0	t
91f52af3-f89a-4d07-aec0-ed511372496f	ELUCIDATE_BALLYHOO_SCYTHE_ROOMMATE	0	22216	0	t
8bc40f0a-efad-490f-98f3-37faeb8fa4d5	GOES_CARBONYL_WOMBAT_KYLE	0	23201	0	t
731f07d5-a607-4e8d-92a4-a001fe38abc7	VERANDA_INSTRUCT_PROXIMATE_CRUISE	0	23202	0	t
9948c81d-7f17-4957-8f73-aef35b4e7f3d	WATERSHED_HEIDELBERG_JOCOSE_POLLOI	0	23203	0	t
3206e87c-5bfd-4ad2-a5f6-7c052378ccdb	CREPE_LOCKIAN_RODEO_BASIDIOMYCETES	0	23204	0	t
68fc78c9-383a-4d02-b0fd-10467c09e912	CONSULT_SUIT_DERATE_DEPORTEE	0	23205	0	t
d3888453-eb85-4fd3-b287-e01ec769bb3d	DANK_SCHEMATIC_WELLINGTON_NITROGENOUS	0	23206	0	t
19324549-0964-4514-8d48-2656147a7b0a	COYPU_HELD_TIDE_HUNDREDTH	0	23207	0	t
87a20c69-ec18-48e1-8cbb-8c0a93391e94	CONVENE_DEVIOUS_PROLATE_LOTUS	0	23208	0	t
a94dc540-dd52-4f42-beda-311f5aa4dec1	ROBERTA_PERGAMON_ARMATURE_FOXHOUND	0	23209	0	t
868434b2-6688-438c-8902-2c5e0046f9e7	APPROPRIATE_IVY_FIREWORK_SPATLUM	0	23210	0	t
bc69da38-106a-4cbc-b2cd-515cd3d65a01	DAMP_ENAMEL_EVASION_SYLVESTER	0	23211	0	t
43d9830c-3165-4554-a250-7bee79ef363c	THEORETIC_NARWHAL_INFLATIONARY_PROGRESSION	0	23212	0	t
21bbcfd4-5f36-49f3-bf89-34107062669f	GOLDSTINE_SALINE_OFFSHORE_PIZZICATO	0	23213	0	t
af309450-380b-4330-91c5-01585b19e981	SPINY_SANDUSKY_INGROWN_MUSHROOM	0	23214	0	t
b911c36f-d2b0-4d6a-9008-18a23a1e43c4	MEREDITH_SEERSUCKER_GRADE_LEE	0	23215	0	t
42bc667f-4ac7-4aad-92f0-210a5d2c2465	AMBIGUOUS_MT_URBANA_ONONDAGA	0	23216	0	t
466ceba9-1afd-4773-b5f5-acef89d44b71	PAPILLARY_EXCISION_COLLATE_SOMETIME	0	23217	0	t
adc27406-3c20-44e1-99da-92e1e132e40d	SEDATE_PONT_BUTTRESS_CASKET	1	organizers	2	t
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (chat_id, url, username, full_name, role, team_id) FROM stdin;
241044762	tg://user?id=241044762	solloballon	ki	user	\N
274594229	tg://user?id=274594229	kislo_sladky	Илья Кислицын	user	\N
474965280	tg://user?id=474965280	TheBlek	Егор	user	\N
476893348	tg://user?id=476893348	h1km4t1ll0	Даниил Долгов	user	\N
2051169652	tg://user?id=2051169652	aloha_kuino	Александр Шушаков	user	\N
409715742	tg://user?id=409715742	notwizzard	Ivan Morgun	user	\N
296976910	tg://user?id=296976910	MurenMurenus	Maksim Kotenkov	admin	adc27406-3c20-44e1-99da-92e1e132e40d
575506876	tg://user?id=575506876	melaroozz	лера	user	adc27406-3c20-44e1-99da-92e1e132e40d
\.


--
-- Name: user_chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_chat_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: results pk__results; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT pk__results PRIMARY KEY (id);


--
-- Name: solved_quiz pk__solved_quiz; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solved_quiz
    ADD CONSTRAINT pk__solved_quiz PRIMARY KEY (id);


--
-- Name: solved_tasks pk__solved_tasks; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solved_tasks
    ADD CONSTRAINT pk__solved_tasks PRIMARY KEY (id);


--
-- Name: task pk__task; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT pk__task PRIMARY KEY (id);


--
-- Name: team pk__team; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT pk__team PRIMARY KEY (id);


--
-- Name: user pk__user; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT pk__user PRIMARY KEY (chat_id);


--
-- Name: results uq__results__id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT uq__results__id UNIQUE (id);


--
-- Name: solved_quiz uq__solved_quiz__id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solved_quiz
    ADD CONSTRAINT uq__solved_quiz__id UNIQUE (id);


--
-- Name: solved_tasks uq__solved_tasks__id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.solved_tasks
    ADD CONSTRAINT uq__solved_tasks__id UNIQUE (id);


--
-- Name: task uq__task__flag; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT uq__task__flag UNIQUE (flag);


--
-- Name: task uq__task__id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT uq__task__id UNIQUE (id);


--
-- Name: task uq__task__name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT uq__task__name UNIQUE (name);


--
-- Name: team uq__team__id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT uq__team__id UNIQUE (id);


--
-- Name: team uq__team__name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT uq__team__name UNIQUE (name);


--
-- Name: team uq__team__token; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT uq__team__token UNIQUE (token);


--
-- Name: user uq__user__chat_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT uq__user__chat_id UNIQUE (chat_id);


--
-- PostgreSQL database dump complete
--


replies = {
    "test_answer": [
        {"type": "text", "text": "Это тестовый <b>диалог</b>"},
        {"type": "photo", "src": "test.png", "caption": "Подпись к фотке"},
        {
            "type": "sticker",
            "id": "CAACAgIAAxkBAAEGRhhjYPSRFJBpTgkS3v2jflNMryZQlgAC1RQAAm6D0UsnSBfubUrPjSoE",
        },
    ],
    "start": [
        {
            "type": "text",
            "text": "🗺️ <b>Hello hunter</b>, I'm <i>Scavenger Hunt Bot</i>. I'll entertain you today.\n\n"
            "🎯 I have prepared an adventure for you, at the end of which you will receive cool prizes! 🎁\n"
            "🔎 You have to join the team of your group. Ask for an invitation token from the head of the group. "
            "He/She can get it from organizers.\n"
            "🥇 Your team has special points which you can earn by completing tasks.\n"
            "🔎 <i>To get more info use <b>/info</b> or type <b>info</b></i>\n"
            "If you're stuck, you can always <b>/cancel</b> or <b>cancel</b> last action.\n\n"
            "Good luck, <b>hunter</b>!",
        }
    ],
    "cancel": [{"type": "text", "text": "sudo rm, action was canceled..."}],
    "support": [
        {"type": "text", "text": "Your problems are NOT my problems, hunter...\n"
                                 "Ok, if you really have a serious problem - ask our team:"
                                 "@MurenMurenus "
                                 "@h1km4t1ll0 "
                                 "@TheBlek "
                                 "@melaroozz "
                                 "to solve it"}
    ],
    "info": [
        {
            "type": "text",
            "text": "🗺️ Hi!\n"
                    "Maybe you wanna ask me - why should you participate in this adventure? The answer is obvious! "
                    "Here you will receive amazing <b>gifts</b> and a huge amount of <b>emotions</b> "
                    "from the tasks that I have prepared\n\n"
                    "<i>Here is the plan to win our competition:</i>\n"
                    "👥️ Join <b>team</b> of your group <i>(you should ask it from the head of the group)</i>\n"
                    "🎯️ Farm <b>points</b>! There are several ways to do this\n\n"
                    "📝️ Use <b>Tasks</b> button or <b>/tasks</b> command to get information about competitions"
                    " which you can get points for\n"
                    "📊️ Also, you can track the other teams activity here: leaderboard.elephahealth.com or by using <b>Scoreboard</b> button "
                    "or <b>/scoreboard</b> command. Let's try to get the first place!\n"
                    "❓ There are secrets inside the NSU with a special <b>FLAG</b> <i>(common string of english words)</i> "
                    "(like THIS_IS_A_FLAG) "
                    " which you should pass to me using <b>Flag</b> button or <b>/flag</b> command\n"
                    "🔈️ I will notify you about all significant events - follow my messages!\n\n"
                    "<i>So, don't waste your time, hunter!</i>",
        }
    ],
    "map": [
        {
            "type": "map",
            "src": ["Map0.jpg", "Map1.jpg", "Map2.jpg", "Map3.jpg", "Map4.jpg", "Map5.jpg"],
            "caption": "It's a map with marked areas where you can find secrets and get points with /flag command\n"
            "Look carefully, who knows what you can find 🕵",
        }
    ],
    "create_team_start": [
        {
            "type": "text",
            "text": "<i>Now you have to choose a name for your team (send it)</i>👁️",
        }
    ],
    "create_team_already_in_team": [
        {
            "type": "text",
            "text": "🤥 O-o-ops! 🤥\n"
            "Don't try to fool me, hunter! You already have a team!\n\n"
            "<i>Use /leave_team to leave your friends-losers</i> 💩",
        }
    ],
    "create_team_name_is_taken": [
        {"type": "text", "text": "O-ho-ho... Smth went wrong, this team name is taken 😵"}
    ],
    "create_team_created": [
        {
            "type": "text",
            "text": "Your team was successfully created!",
        }
    ],
    "join_team_token_invalid": [
        {
            "type": "text",
            "text": "Pu-pu-pu... Your invite token is <b>invalid</b>! Try one more time or use /support command",
        }
    ],
    "leave_team_not_in_team": [
        {
            "type": "text",
            "text": "To leave team you have to be in team XD",
        }
    ],
    "join_team_full_team": [
        {
            "type": "text",
            "text": "Hmm.. This team is full, if you think that it is mistake - use /support",
        }
    ],
    "join_team_already_in_team": [
        {
            "type": "text",
            "text": "Sorry, you can join new team only after leaving your current team",
        }
    ],
    "join_team_joined": [
        {
            "type": "text",
            "text": "Congrats! Now you are ready to farm points and win some prizes with your groupmates! 👩🏿‍🌾",
        },
    ],
    "leave_team_left": [
        {
            "type": "text",
            "text": "Now you are a loner 💪",
        },
    ],
    "join_team_start": [
        {
            "type": "text",
            "text": "Ok, give me your invitation token. Ask your group leader about it.",
        },
    ],
    "no_team_action": [
        {
            "type": "text",
            "text": "Hey, hunter! To use this command you have to be in team!",
        },
    ],
    "send_flag": [
        {
            "type": "text",
            "text": "Ok, send me your flag 👉👈",
        },
    ],
    "invalid_flag": [
        {"type": "text", "text": "Oh, terrible news, hunter... This flag is INVALID! 😎"},
    ],
    "solve_task_start": [
        {
            "type": "text",
            "text": "Your next message will be forwarded to the manager of this task to check the answer, let's send it to me"
        },
    ],
    "solution_sent": [
        {
            "type": "text",
            "text": "Your solution was forwarded to the task manager, wait for results"
        },
    ],
    "task_usage_exceeded": [
        {
            "type": "text",
            "text": "Hm, bad try, someone passed this task faster than you",
        },
    ],
    "used_flag": [
        {
            "type": "text",
            "text": "This task has already been solved by your team",
        },
    ],
    "tasks_types": "❗ <b>Tasks</b> ❗\n\n"
                   "<i>Here you can see 7 types of competitions:</i>\n"
                   "🟢️<b>In Real Life tasks</b>\n"
                   "There is a description of offline tasks that are located somewhere in NSU (or not)\n"
                   "🟢️<b>In Bot tasks</b>\n"
                   "Some tasks, that can be solved online in telegram, but we cannot define their actual type... "
                   "So yeah, they're just InBot tasks\n"
                   "🟢️<b>Cosplay</b>\n"
                   "Here you have to show imagination and creativity, creating parodies of frames from famous films\n"
                   "🟢️<b>Secrets</b>\n"
                   "Secrets... secrets... secrets...\n"
                   "🟢️<b>Song summarization</b>\n"
                   "Listen to some cool songs and describe them\n"
                   "⌛️️<b>Rhyme time</b>\n"
                   "Dreaming about being a poet? No? Nevermind..."
                   "Whatever, try these tasks, they expire after only one solution!!!\n"
                   "HURRY UP AND BE THE FIRST!!!\n"
                   "❓️<b>Quiz</b>\n"
                   "Answer fast and flawless, get your points!\n\n"
                   "<i>Tap the buttons to get more info</i>",
    "online_tasks_description": "❕ <b>InBot tasks</b> ❕\n\n"
                                "There are some tasks that can be solved right there only with your imagination."
                                "Don't worry, these tasks are no less interesting than others!\n"
                                "Have fun and get points!\n\n",
    "offline_tasks_description": "❕ <b>IRL tasks</b> ❕\n\n"
                                 "These tasks should be completed offline (just have fun with your groupmates)."
                                 "Some of them are checked by teachers in different rooms (check descriptions), "
                                 "some of them are checked online by organizers team (send your solutions to us and get point).\n"
                                 "Good luck!\n\n",
    "cosplay_tasks_description": "❕ <b>Cosplay tasks</b> ❕\n\n"
                                 "Repeat the scene from the movie and send the photo using <b>Solve</b> button\n"
                                 "Manager will evaluate it and give you some points (up to 3)\n\n",
    "secrets_tasks_description": "❕ <b>Secrets</b> ❕\n\n"
                                 "Secrets are like <i>easter eggs</i>, they might be anywhere! "
                                 "The Map will help you to find some of them. DO NOT DESTROY SECRETS! It is punishable\n\n"
                                 "<i>Use /flag command to pass a special string from the secret</i> 🙊",
    "songs_tasks_description": "❕ <b>Song summarization tasks</b> ❕\n\n"
                                 "Listen to songs and try to summarize them, send us your answer using <b>Solve</b> button\n"
                                 "Out team will evaluate it and give you some points\n\n",
    "rhymes_tasks_description": "❕ <b>Rhymes time tasks</b> ❕\n\n"
                                 "Try yourself in poetry (Not in Python framework ;) )!\nCreate a sentence that rhymes with the word and send us using <b>Solve</b> button\n"
                                 "Our team will evaluate it and give you some points\n\n",
    "casino_start": "🎰 <b>Casino</b> 🎰\n\n"
                    "HA-HA-HA! Here you can lost all your points! "
                    "Yeah, of course you also can earn sth from this game\n"
                    "<i>Choose amount of points that you will bet</i>",
    "casino_choose_option": "🎰 <b>Casino</b> 🎰\n\n"
                            "Now you have to choose one of these options\n"
                            "▪️RED & BLACK has x2 multiplayer\n"
                            "▪️GREEN is more rare and it has x10 multiplayer\n\n"
                            "<i>You will lose the bet points "
                            "if the selected option does not match the result of the spin</i>",
    "casino_wait": "Wait pls.",
    "rofls": [
          "The student walked through NSU, saw a deadline burning, step into it and burned out.",
          "Stirlitz was good at rofls. There is no joke. He was.",
          "99 dog wished to become cats and the 100th dog wished they all become dog again.",
          "A cat asked its owner What is nuance.\nSit on my lap said the owner\nNow you have ..........\nAnd I have.......\nbut there is a nuance...",
          "Someone knocked 0 times at the door\nA cat - thought Stirlitz",
          "100 cats were crossing a desert and met a genie\nall of them didnt know what they wanted",
          "A burning tank crashed into a huge blue cat. The joke is an exersize",
          "JOKING_INSTEAD_OF_WORKING",
          "a Jewish cat was walking by, saw a bowl of food, ate, thought - not enough",
          "a cat... Ah I forgot the joke nevermind)"
    ]
}

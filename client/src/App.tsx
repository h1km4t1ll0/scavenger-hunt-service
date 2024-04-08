import {useMemo} from 'react'

import './App.css'
import {Api} from "./api.ts";
import ApiProvider from "./providers/ApiProvider.ts";
import {LeaderboardPage} from "./pages/Leaderboard.tsx";

function App() {
    const api = useMemo(
        () => new Api(import.meta.env.VITE_API_URL),
        [import.meta.env.VITE_API_URL]
    );

    return (
        <ApiProvider value={api}>
            <LeaderboardPage/>
        </ApiProvider>
    );
}

export default App

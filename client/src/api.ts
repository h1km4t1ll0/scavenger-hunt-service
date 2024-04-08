import axios from "axios";


export class Api {
    private url: string = '';
    public constructor (url: string) {
        this.url = url;
    }

    public async getLeaderboard() {
        return await axios.get<[x: { team: string, points: number }]>(
            this.url + 'v1/leaderboard'
        );
    }
}

import axios from "axios";


export class Api {
    private url: string = '';

    public constructor(url: string) {
        this.url = url;
    }

    public async getLeaderboard() {
        try {
            const res =  await axios.get<{
                data: [x: { team: string, points: number }],
                code: number
            }>(
                this.url + 'v1/leaderboard'
            );
            return res.data;
        } catch (e) {
            return new Promise<{
                data: [x: { team: string, points: number }],
                code: number
            }>(
                () => (
                    {
                        data: [],
                        code: 500
                    }
                )
            );
        }
    }
}

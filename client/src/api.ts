import axios from "axios";


export class Api {
    private url: string = '';

    public constructor(url: string) {
        this.url = url;
    }

    public async getLeaderboard(): Promise<{
        data: [x: { team: string, points: number }] | null,
        code: number
    }> {
        try {
            const res = await axios.get<{
                data: [x: { team: string, points: number }],
                code: number
            }>(
                this.url + 'v1/leaderboard'
            );
            return res.data;
        } catch (e) {
            console.log(e)
            return new Promise<{
                data: null,
                code: number
            }>(
                (resolve) => resolve(
                    {
                        data: null,
                        code: 500
                    }
                )
            );
        }
    }
}

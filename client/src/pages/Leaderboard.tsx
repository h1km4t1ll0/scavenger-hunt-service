import {
    useCallback, useEffect, useState,
} from 'react';
import {useApi} from "../providers/ApiProvider.ts";
import {Skeleton, Space, Typography, Image, Col, Flex, Result} from "antd";
import logo from '../assets/logo.jpg';

export const LeaderboardPage = () => {
    const api = useApi();
    const [
        leaderboard,
        setLeaderboard
    ] = useState<[x: { team: string, points: number }] | null>(null);
    const [err, setErr] = useState<boolean>(false);
    const load = useCallback(async () => {
        const leaderboardData = await api.getLeaderboard();

        if (leaderboardData.code !== 200 || leaderboardData.data === null) {
            setErr(true);
            return;
        }

        setErr(false);
        setLeaderboard(leaderboardData.data);
    }, []);

    useEffect(() => {
        load();
    }, []);

    useEffect(() => {
        const interval = setInterval(() => {
            load();
        }, 10000);
        return () => {
            if (interval) {
                clearInterval(interval);
            }
        };
    }, []);
    if (err) {
        return (
            <Result
                status="500"
                title="500"
                subTitle="Sorry, something went wrong."
            />
        );
    }
    if (!leaderboard) {
        return (
            <Space direction="vertical" size="small">
                <Image
                    width="70%"
                    preview={false}
                    src={logo}
                />
                <Typography.Title>
                    SCOREBOARD
                </Typography.Title>
                <Flex justify="space-around" gap="middle" align="start">
                    <Col>
                        <Typography.Title level={2}>
                            GROUP
                        </Typography.Title>
                    </Col>
                    <Col>
                        <Typography.Title level={2}>
                            POINTS
                        </Typography.Title>
                    </Col>
                </Flex>
                <Skeleton active paragraph={{rows: 2}}/>
            </Space>)
    }

    return (
        <Space direction="vertical">
            <Image
                width="50%"
                preview={false}
                src={logo}
            />
            <Typography.Title>
                SCOREBOARD
            </Typography.Title>
            <Flex justify="space-around" gap="middle" align="start">
                <Col>
                    <Typography.Title level={2}>
                        GROUP
                    </Typography.Title>
                </Col>
                <Col>
                    <Typography.Title level={2}>
                        POINTS
                    </Typography.Title>
                </Col>
            </Flex>
            {
                leaderboard.map(
                    (each) => {
                        return (
                            <Flex justify="space-around" gap="middle" align="start">
                                <Col>
                                    <Typography.Title level={2}>
                                        {each.team}
                                    </Typography.Title>
                                </Col>
                                <Col>
                                    <Typography.Title level={2}>
                                        {each.points}
                                    </Typography.Title>
                                </Col>
                            </Flex>
                        )
                    }
                )
            }
        </Space>
    );
}

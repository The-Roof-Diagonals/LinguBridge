import { Button, Col, Collapse, Row, Space, Statistic, Typography } from "antd";
import { DownloadOutlined } from "@ant-design/icons";
import "./TaskItem.css";
import axios from "axios";
import { BASE_URL } from "./App";
import { useEffect, useState } from "react";

interface Props {
  taskId: string;
  name: string;
  updated: Date;
  created: Date;
  currActive: number;
  getLanguage: () => string;
}

interface TaskDetail {
  similarityScore: SimilarityScore;
  translatedText: string;
  originalText: string;
  originalLanguage: string;
}

interface SimilarityScore {
    gpt: number;
    spacy: number;
    tfidf: number;
}

export const TaskItem = (props: Props) => {
  const [taskDetail, setTaskDetail] = useState<TaskDetail>();
  const [loading, setLoading] = useState(false);
  const [active, setActive] = useState(false);

  const getTaskDetail = async () => {
    axios
      .get(`${BASE_URL}/tasks/${props.taskId}/file/${props.getLanguage()}`)
      .then((res) => {
        const taskDetail: TaskDetail = {
          originalLanguage: res.data.original_language,
          originalText: res.data.original_text,
          similarityScore: res.data.similarity_score,
          translatedText: res.data.translated_text,
        };
        setTaskDetail(taskDetail);
        setLoading(false);
      });
  };

  const onChange = (key: string | string[]) => {
    if (key.length === 1) {
      setLoading(true);
      getTaskDetail();
      setActive(true);
    } else {
      setActive(false);
    }
  };

  useEffect(() => {
    if (active) {
      getTaskDetail();
    }
  }, [props.getLanguage]);


  const { Panel } = Collapse;
  return (
    <Collapse
      size="large"
      ghost
      expandIconPosition="end"
      bordered={false}
      onChange={onChange}
    >
      <Panel header={<div>{props.name}</div>} key={1}>
        <p>
          {loading ? (
            <Typography.Text type="secondary">Loading...</Typography.Text>
          ) : (
            props.getLanguage() === taskDetail?.originalLanguage ? (
                <Row>
                    <Col span={24}>
                        <Typography.Text type="secondary">
                            Original Text:
                        </Typography.Text>
                        <Typography.Paragraph>
                            {taskDetail?.originalText}
                        </Typography.Paragraph>
                    </Col>
                </Row>
            ) : (
                <>
                <Row>
                    <Typography.Text type="secondary">
                        Translated Text:
                    </Typography.Text>
                    <Typography.Paragraph>
                        {taskDetail?.translatedText}
                    </Typography.Paragraph>
                </Row>
                <Row>
                    <Typography.Text type="secondary">
                        Original Text (from {taskDetail?.originalLanguage}):
                    </Typography.Text>
                    <Typography.Paragraph>
                        {taskDetail?.originalText}
                    </Typography.Paragraph>
                </Row>
                <Row>
                    <Statistic title="Similarity Score (GPT):" value={taskDetail?.similarityScore?.gpt} />
                </Row>
                <Row>
                    <Statistic title="Similarity Score (GPT):" value={taskDetail?.similarityScore?.spacy} />
                </Row>
                <Row>
                    <Statistic title="Similarity Score (GPT):" value={taskDetail?.similarityScore?.tfidf}/>
                </Row>

                </>
                )
            )}
          {/* <br />
          <br />
          {taskDetail?.originalText}
          <br />
          {taskDetail?.similarityScore?.gpt} */}
        </p>
        {/* <Space size={8} wrap>
            <Button type="primary" icon={<DownloadOutlined />}>PDF-Report</Button>
            <Button type="primary" icon={<DownloadOutlined />}>Translated</Button>
            <Button type="primary" icon={<DownloadOutlined />}>Original-Files</Button>
        </Space> */}
      </Panel>
    </Collapse>
  );
};

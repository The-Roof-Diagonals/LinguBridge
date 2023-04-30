import { Button, Collapse, Input, Space, Upload } from "antd";
import { AudioOutlined, CameraOutlined } from "@ant-design/icons";
import "./TaskItem.css";
import axios from "axios";
import { BASE_URL } from "./App";

interface Props {
    name: string;
    taskId: string;
    setTaskText: (text: string) => void;
    getLanguage: () => string;
}


export const CurrentTaskItem = (props: Props) => {
    const { Panel } = Collapse;

    const uploadFile = async (file: File) => {
        const formData = new FormData();
        formData.append("file", file);
        return axios.post(`${BASE_URL}/tasks/${props.taskId}/file/${props.getLanguage()}`, formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }).then((res) => {
            console.log(res);
            return res.statusText;
        });
    }


  return (
    <Collapse size="large" ghost expandIconPosition="end" bordered={false} activeKey={1}>
      <Panel header={<div>{props.name}</div>} key={1}>
        <Space size={8} wrap>
            <Input.TextArea placeholder="Please describe your task here" onChange={(e) => props.setTaskText(e.currentTarget.value)}/>
            <Upload accept="image/*" action={`${BASE_URL}/tasks/${props.taskId}/file/${props.getLanguage()}`} >
                <Button type="primary" icon={<CameraOutlined />}>Upload Notes</Button>
            </Upload>
            <Upload accept="audio/*" capture="user" action={uploadFile}>
                <Button type="primary" icon={<AudioOutlined />}>Upload Audio</Button>
            </Upload>
        </Space>
      </Panel>
    </Collapse>
  );
};

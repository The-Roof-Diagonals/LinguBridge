import { Row, Col, Steps, Button } from "antd";
import { useNavigate, useParams } from "react-router-dom";
import { TaskItem } from "./TaskItem";
import { CurrentTaskItem } from "./CurrentTaskItem";
import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { BASE_URL } from "./App";

interface Task {
  id: string;
  projectId: string;
  name: string;
  active: boolean;
  created: Date;
  updated: Date;
}


export const Task = (props: {language: string, getLanguage: () => string }) => {
  const navigate = useNavigate();
  const { projectId } = useParams();
  const [ items, setItems ] = useState();
  const [ numFinishedTasks, setNumFinishedTaks ] = useState(0);

  const getLanguage = useMemo(() => {
    console.log(props.language);
    return () => props.language;
  }, [props.language]);


  const [ taskText, setTaskText ] = useState("");

  const postTaskText = () => {
    axios.put(`${BASE_URL}/tasks/${numFinishedTasks + 1}`, { text: taskText, language: props.language }).then((res) => {
      setNumFinishedTaks(numFinishedTasks + 1);
      setTaskText("");
      navigate("/")
    });
}
  
  useEffect(() => {
    axios.get(`${BASE_URL}/projects/${projectId}/tasks`).then((res) => {
      const numFinishedTasks = res.data.filter((task: Task) => !task.active).length;
      const taskItems = res.data.map((task: Task) => {
        return { title: <TaskItem taskId={task.id} name={task.name} created={task.created} updated={task.updated} getLanguage={() => getLanguage()} currActive={numFinishedTasks}/>}
      });

      const curTask = res.data[numFinishedTasks]
      if(numFinishedTasks < res.data.length){
        taskItems[numFinishedTasks] = { title: <CurrentTaskItem name={curTask.name} taskId={curTask.id} getLanguage={() => getLanguage()} setTaskText={setTaskText} /> }
      }
      setItems(taskItems);
      setNumFinishedTaks(numFinishedTasks);
    });
  }, [getLanguage, numFinishedTasks]);

  return (
    <Col style={{ display: "flex", flexDirection: "column", height: "100%", marginBottom: "50px"}}>
        <Row style={{margin: "16px"}}>
          <Steps direction="vertical" current={numFinishedTasks} items={items}/>
        </Row>
        <Row style={{ position: "fixed", bottom: "0",  width: "100%", backgroundColor: "#ffffff", border: "1px"}}>
            <Button type="primary" style={{ width: "100%", margin: "16px"}} onClick={postTaskText}>Finish current task</Button>
        </Row>
    </Col>
  );
};

import { Header } from "antd/es/layout/layout";
import './NewHeader.css';
import { Col, Row } from "antd";
import Flags from "./Flags";
import "./Flags.css"

const NewHeader = (props:any) => {
  //The Pipe Layerers :(((
  return (
    <Row className='header'>
      <Col className='column'>
        <Header className="header" style={{ color: 'white' }}>Work I Did</Header>
      </Col>
      <Col className="flag">
        <Flags setLanguage={props.setLanguage}></Flags>
      </Col>
    </Row>
  );
};

export default NewHeader;
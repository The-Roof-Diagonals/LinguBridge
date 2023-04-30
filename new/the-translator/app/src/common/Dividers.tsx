import { Col, Row } from "antd";
import AppointmentDate from "./AppointmentDate";
import "./Dividers.css"

const Dividers = (props : any) => {
    return (
        <Row className="divider" >
            <Col style={{padding: 16}}>
                <AppointmentDate date={props.client.date}/>
            </Col>
            <Col className="client-information">
                <div className="client-name">{props.client.name}</div>
                <div className="adresse">{props.client.address}</div>
            </Col>
        </Row>
    )
}

export default Dividers;
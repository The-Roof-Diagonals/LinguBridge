import { Button, List } from 'antd';
import './ListOfClients.css'
import { useEffect, useState } from 'react';
import Dividers from "./Dividers"
import { useNavigate } from 'react-router-dom';
import axios from 'axios'

interface Client {
    name: string;
    address: string;
    date: string;
}

const mockClients = [{
    name: "Adrian Averwald",
    address: "Königsbergerstraße 13",
    date: new Date(2023, 4, 30, 10, 30).toISOString().slice(0, 19).replace('T', ' '),
}]

const ListOfClients = () => {
    const navigate = useNavigate();
    const [clients, setClients] = useState<Client[]>(mockClients);
    const nextPage = () => {
        navigate("/1")
    }

    useEffect(() => {
        axios.get("http://10.7.0.7:5000/projects").then(data => data.data).then(data => {
            console.log(data)
            setClients(data)
        })
    }, [])

    async function onSubmit(client: Client) {
        try {
            const response = await axios.post('http://10.7.0.7:5000/projects', client);
            console.log(response);
            setClients((prevClients: Client[]) => {
                return [client, ...prevClients];
            });
        } catch (err) {
            console.error(err);
        }
    }
 
    async function onReceive() {
        try {
            const response = await axios.get('http://10.7.0.7:5000/projects');
            console.log(response);
        } catch (err) {
            console.error(err);
        }
    }

    const addItem = () => {
        onSubmit(mockClients[0]);
    }

    return (
        <List className='list'>
            {(clients && Array.isArray(clients)) ?
                clients.map(client => {
                    return (
                        <List.Item onClick={() => nextPage()}>
                            <Dividers client={client} />
                        </List.Item>)
                }) : 'No new Projects currently :)'
            }
        </List>
    );
};

export default ListOfClients
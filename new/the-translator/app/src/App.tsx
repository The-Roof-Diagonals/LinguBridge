import { Route, Routes } from 'react-router-dom';
import { Layout, Space } from 'antd';
import { Task } from './Task';
import './App.css';
import NewHeader from './NewHeader'
import ListOfClients from './common/ListOfClients';
import { useDebugValue, useEffect, useState } from 'react';

export const BASE_URL = "http://10.7.0.7:5000";

function App() {
  const { Content } = Layout;
  const [language, setLanguage] = useState('en')

  useEffect(() => {
    console.log(language)
  }, [language])
  
  return (
    <div className="App">
      <Space direction="vertical" style={{ width: '100%' , height: '100%'}} size={[0, 48]}>
        <Layout>
          <NewHeader setLanguage={(value: string) => setLanguage(value)} />
          <Content>
            <Routes>
              <Route path="/" element={<ListOfClients />} />
              <Route path="/:projectId" element={<Task language={language} getLanguage={() => {console.log(language); return language}} />} />
            </Routes>
          </Content>
        </Layout>
      </Space>
    </div>
  );
}

export default App;

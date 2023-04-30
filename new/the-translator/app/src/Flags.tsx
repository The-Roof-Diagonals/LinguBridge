import { Image } from 'antd';
import { Select } from 'antd';

const { Option } = Select;


const Flags = (props:any) => {
    const handleChange = (value: string) => {
        props.setLanguage(value);
    }

    return (
        <div>
            <Select defaultValue="en" style={{ width: 92 }} onChange={handleChange}>
                <Option value="en">
                    <Image
                        src="flags/UK.png"
                        height={30}
                        width={50}
                        preview={false}
                    ></Image>
                </Option>
                <Option value="de">
                    <Image
                        src="flags/Germany.png"
                        height={30}
                        width={50}
                        preview={false}
                    ></Image>
                </Option>
                <Option value="pl">
                    <Image
                        src="flags/Poland.png"
                        height={30}
                        width={50}
                        preview={false}
                    ></Image>
                </Option>
                <Option value="ukr">
                    <Image
                        src="flags/Ukraine.png"
                        height={30}
                        width={50}
                        preview={false}
                    ></Image>
                </Option>
                <Option value="cze">
                    <Image
                        src="flags/Czech.png"
                        height={30}
                        width={50}
                        preview={false}
                    ></Image>
                </Option>
                <Option value="it">
                    <Image
                        src="flags/Italy.png"
                        height={30}
                        width={50}
                        preview={false}
                    ></Image>
                </Option>
            </Select>
        </div>
    )
};

export default Flags;


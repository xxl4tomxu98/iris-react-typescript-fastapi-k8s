import React, { useState } from 'react';
import './App.css';
import {Col, Container, Row, Button, Form} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.css';

interface FormData {
    sepalLength: number,
    sepalWidth: number,
    petalLength: number,
    petalWidth: number
}

const App = () => {
    const [isLoading, setIsloading] = useState<boolean>(false);
    const [formData, setFormData] = useState<FormData>({
        sepalLength: 4.0,
        sepalWidth: 2.0,
        petalLength: 1.0,
        petalWidth: 0.0
    });
    const [result, setResult] = useState<string>("");


    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value: number = event.target.valueAsNumber;
        const name: string = event.target.name;
        let inputData: FormData = {...formData};
        inputData[name as keyof FormData]=value;
        setFormData(inputData);
    }

    const handlePredictClick = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {        
        const url = "http://127.0.0.1:8000";
        setIsloading(true);
        fetch(url,
        {
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(response => {
            setResult(response.result);
            setIsloading(false);
        });
    }

    const handleCancelClick = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        setResult("");
    }


    let sepalLengths = [];
    for (let i = 4; i <= 7; i = +(i + 0.1).toFixed(1)) {
        sepalLengths.push(<option key = {i} value = {i}>{i}</option>);
    }
    let sepalWidths = [];
    for (let i = 2; i <= 4; i = +(i + 0.1).toFixed(1)) {
        sepalWidths.push(<option key = {i} value = {i}>{i}</option>);
    }
    let petalLengths = [];
    for (let i = 1; i <= 6; i = +(i + 0.1).toFixed(1)){
        petalLengths.push(<option key = {i} value = {i}>{i}</option>);
    }
    let petalWidths = [];
    for (let i = 0.1; i <= 3; i = +(i + 0.1).toFixed(1)) {
        petalWidths.push(<option key = {i} value = {i}>{i}</option>);
    }

    return (
        <Container>
            <div>
                <h1 className="title">Iris Plant Classifier</h1>
            </div>
            <div className="content">
            <Form>
                <Row>
                    <Form.Group as={Col}>
                        <Form.Label>Sepal Length</Form.Label>
                        <Form.Control
                            as="select"
                            value={formData.sepalLength}
                            name="sepalLength"
                            onChange={handleChange}>
                            {sepalLengths}
                        </Form.Control>
                    </Form.Group>
                    <Form.Group as={Col}>
                        <Form.Label>Sepal Width</Form.Label>
                        <Form.Control
                            as="select"
                            value={formData.sepalWidth}
                            name="sepalWidth"
                            onChange={handleChange}>
                            {sepalWidths}
                        </Form.Control>
                    </Form.Group>
                </Row>
                <Row>
                    <Form.Group as={Col}>
                        <Form.Label>Petal Length</Form.Label>
                        <Form.Control
                            as="select"
                            value={formData.petalLength}
                            name="petalLength"
                            onChange={handleChange}>
                            {petalLengths}
                        </Form.Control>
                    </Form.Group>
                    <Form.Group as={Col}>
                        <Form.Label>Petal Width</Form.Label>
                        <Form.Control
                            as="select"
                            value={formData.petalWidth}
                            name="petalWidth"
                            onChange={handleChange}>
                            {petalWidths}
                        </Form.Control>
                    </Form.Group>
                </Row>
                <Row>
                    <Col>
                        <Button
                            //block
                            variant="success"
                            disabled={isLoading}
                            onClick={!isLoading ? handlePredictClick : undefined}>
                            { isLoading ? 'Making prediction' : 'Predict' }
                        </Button>
                    </Col>
                    <Col>
                        <Button
                            //block
                            variant="danger"
                            disabled={isLoading}
                            onClick={handleCancelClick}>
                            Reset prediction
                        </Button>
                    </Col>
                </Row>
            </Form>
            {result === "" ? null :
                (<Row>
                    <Col className="result-container">
                        <h5 id="result">{result}</h5>
                    </Col>
                </Row>)
            }
            </div>
        </Container>
    );

}

export default App;


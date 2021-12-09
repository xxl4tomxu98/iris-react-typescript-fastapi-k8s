# DPS

The AI Document Processing Solution (DPS) is an internally developed modular platform providing clients and engagement teams with tools for automated data capture from various document formats. DPS delivers value to clients and organizations through reusability of document processing components, facilitating delivery efficiency and cost savings. The key outcome of the platform will be to extend the value of current and future document processing investments to the broader organization.

## Problem Statement

Most enterprise data is in an unstructured format. Internal and external organizations need to process and transform the documents into structured data to understand and unlock value within unstructured document data. The demand for document processing capabilities continues to grow as nearly all business processes generate documents.
In previous engagements, document processing components were independently developed, thereby limiting the timeframe for solution lifecycle and reusability. This has potentially led to duplicated efforts for core data transformation components such as OCR, data extraction, and sentiment analysis.

## Folder Structure

    - docker | dockerfile config
    - fastapi | webserver
    - tests | unit tests for application
    - frontend | React UI front-end

## Install Requirements

    ./env/bin/activate
    pip install -r requirements.txt

## Launch BackEnd

    cd fastapi/
    python3 main.py

## Launch FrontEnd

    cd frontend
    npm install
    npm start

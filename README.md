# Beauty Salon Booking Bot

A Telegram bot for managing beauty salon appointments.

## Features

- Service and category selection
- Personnel selection
- Appointment date and time selection
- Appointment booking and cancellation
- Personnel availability management
- Admin commands for managing salon services and appointments

## Technologies

- Python
- Telegram Bot API (`pyTelegramBotAPI`)
- MySQL
- `jdatetime`

## Project Structure

- `main.py` — Main bot logic and appointment workflow
- `DQL.py` — Database queries for retrieving data
- `DML.py` — Database operations for inserting, updating, and deleting data
- `DDL.py` — Database and table definitions
- `texts.py` — Bot messages and text constants
- `requirements.txt` — Project dependencies
- `.env` — Environment variables and sensitive configuration

## Security

Sensitive information, such as API tokens and database credentials, should be stored securely and must not be uploaded to the public repository.

## Project Status

This project is developed for beauty salon appointment management using Telegram.
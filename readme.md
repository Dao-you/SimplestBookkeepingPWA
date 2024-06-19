# SimplestBookkeepingPWA

SimplestBookkeepingPWA is a minimalist, cloud-based bookkeeping application designed to simplify the task of financial record-keeping. This project features a user-friendly interface, cloud storage, and Progressive Web App (PWA) capabilities, making it accessible from any device. The application supports responsive design, one-handed use, and includes import/export functionality for easy data management.

## Key Features

1. **Super Simple Interface**:
   - Clean and intuitive interface designed to make bookkeeping easy and less cumbersome.

2. **Cloud-Based Storage**:
   - All user data is stored securely on the server, allowing access from any device with an internet connection.

3. **Progressive Web App (PWA) Design**:
   - Accessible via a web browser or installable as a standalone app on devices.

4. **Responsive Web Design (RWD)**:
   - Automatically adjusts layout to suit any screen size, ensuring optimal usability on all devices.

5. **One-Handed Use**:
   - Interface optimized for single-handed operation on mobile devices.

6. **Import and Export Capabilities**:
   - Users can import and export financial data in spreadsheet format for easy data management and backup.

7. **Dark Mode**:
   - Supports dark mode for comfortable use at night.

## Installation

To install and run the SimplestBookkeepingPWA, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/Dao-you/SImplestBookkeepingPWA.git
   cd SimplestBookkeepingPWA
   ```

2. Install the necessary dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Configure HTTPS:
   - PWA functionalities require HTTPS. To add your SSL certificate, update the `SSLconfig.json` file with your certificate paths:
     ```json
     {
       "certfile": "path/to/your/cert.pem",
       "keyfile": "path/to/your/key.pem"
     }
     ```
   - The program will attempt to read the SSL configuration from `SSLconfig.json`. If it fails, it will run using unencrypted HTTP, but PWA features will be unavailable.
   - For more information on obtaining SSL certificates, you can refer to these guides:
     - [Let's Encrypt](https://letsencrypt.org/getting-started/)
     - [SSL for Free](https://www.sslforfree.com/)

4. Run the application:
   ```
   python bot.py
   ```

5. Network Settings:
   - Ensure proper network settings to allow access from other devices. Refer to these guides for more details:
     - [Port Forwarding](https://www.howtogeek.com/66214/how-to-forward-ports-on-your-router/)
     - [Setting Up a Static IP Address]()

## User Guide

### Frontend

- The home page allows users to input transactions in the format \<price>/\<description>.
- Custom transaction type options can be added via the provided links in the bottom of UI.
- Submitting an empty for displays the transaction records.

For more information and detailed documentation, visit the [GitHub repository](https://github.com/Dao-you/SimplestBookkeepingPWA).

# Simplest Bookkeeping PWA

![App Icon](./static/icons/icon_144.png)

## Introduction

Simplest Bookkeeping PWA is a progressive web application designed to help you manage your personal finances efficiently. This application allows you to track your income and expenses with ease, providing a user-friendly interface and essential features for everyday bookkeeping.

## Features

- **Transaction Recording**: Log various income and expense entries.
- **CSV Export**: Export your transaction records to a CSV file for further analysis.
- **Category Management**: Use default categories or create custom ones to organize your transactions.
- **Offline Functionality**: Access and use the app without an internet connection, with data syncing upon reconnection.

## Benefits of PWA

- **Offline Availability**: Continue using the app even when offline. Data syncs when the connection is restored.
- **Easy Installation**: Install directly from your browser without needing an app store.
- **Automatic Updates**: Always use the latest version without manual updates.
- **Improved Performance**: Enhanced loading speeds through caching technology for a better user experience.

## Responsive Web Design Techniques

- **Flexible Layouts**: Utilizes CSS flexbox and grid for adaptive layouts.
- **Media Queries**: Adjusts styles based on device sizes for optimal viewing.
- **Relative Units**: Employs percentages, em, and rem for scalable designs.
- **Responsive Images**: Uses `srcset` to load images suitable for different resolutions.

## Installation and Running the Project

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/Dao-you/SimplestBookkeepingPWA.git
    cd SimplestBookkeepingPWA
    ```

2. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Obtain an SSL Certificate**:
   You need a secure certificate to run your PWA on HTTPS. You can obtain a free SSL certificate from [Let's Encrypt](https://letsencrypt.org/).

4. **Place Certificate Files**:
   Copy your SSL certificate files (e.g., `fullchain.pem` and `privkey.pem`) to a directory such as `certs/`.

5. **Create a Configuration File**:
   Create a file named `config.py` in your project directory with the following content:
    ```python
    SSL_CERT_PATH = 'certs/fullchain.pem'
    SSL_KEY_PATH = 'certs/privkey.pem'
    ```

6. **Run the Development Server**:
    ```sh
    python app.py
    ```

7. **Access the Application**:
    Open your browser and navigate to `https://localhost:5000`.

## Usage

1. **Record Transactions**: Navigate to the transaction page and input your income or expenses.
2. **Export Data**: Go to the settings and select the option to export your transaction data to a CSV file.
3. **Manage Categories**: Add, edit, or delete categories to better organize your finances.

For more detailed information, please visit the [GitHub repository](https://github.com/Dao-you/SImplestBookkeepingPWA).

## Contributing

Feel free to fork this repository, submit issues, and create pull requests. Your contributions are welcome!

## License

This project is licensed under the MIT License.

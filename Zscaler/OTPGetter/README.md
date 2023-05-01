
# ZPA Connector OTP Generator

Retrieve OTP for a certain user using user's udid.




## Environment Variables

To run this project, you will need to add the following environment variables.

```bash
export CONN_API_KEY="API_KEY"
```

```bash
export CONN_SC_KEY="SECRET_KEY"
```



## Usage

```bash
./get_otp.py --udid "253B446D-D4A2-1F3E-DFAC-A51EDA415A55:705"
```

## API Reference

#### Authentication

```http
GET /papi/auth/v1/login
```

#### Get OTP
```http
GET //papi/public/v1/getOtp?udid={udid}
```




## Documentation

[Documentation](https://help.zscaler.com/client-connector/getting-started-client-connector-api)


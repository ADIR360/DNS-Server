# DNS-Server
Developing a DNS server and filter on a computer involves creating a system that resolves domain names and can selectively block or redirect certain domains. This can enhance security, reduce ads, and control access to web content. Below is a comprehensive guide on setting up your own DNS server and filter.

### **Overview**

- **What is a DNS Server?**
  - A DNS (Domain Name System) server translates human-readable domain names (like www.example.com) into IP addresses that computers use to communicate.
  
- **Why Develop a DNS Filter?**
  - **Ad Blocking**: Prevent unwanted ads by blocking ad domains.
  - **Parental Control**: Block inappropriate content for children.
  - **Security**: Prevent access to malicious sites.
  - **Network Efficiency**: Reduce unnecessary bandwidth usage by blocking unwanted domains.

- **Use Cases:**
  - Home networks for ad-free browsing.
  - Schools or libraries to enforce content restrictions.
  - Businesses to enhance security against phishing.

### **Step-by-Step Guide**

#### **1. Prepare Your Environment**

1. **System Requirements**:
   - A computer running Linux (Ubuntu or Debian recommended).
   - Administrative (root) access.
   - Internet connection.

2. **Install Required Packages**:
   - Install necessary packages using the package manager:
     ```bash
     sudo apt-get update
     sudo apt-get install dnsutils dnsmasq curl
     ```

#### **2. Set Up the DNS Server**

1. **Install `dnsmasq`**:
   - `dnsmasq` is a lightweight DNS forwarder and DHCP server suitable for small networks.
     ```bash
     sudo apt-get install dnsmasq
     ```

2. **Configure `dnsmasq`**:
   - Open the configuration file:
     ```bash
     sudo nano /etc/dnsmasq.conf
     ```
   - Add or modify settings for DNS resolution and filtering:
     ```bash
     # Listen on all interfaces
     interface=eth0
     listen-address=127.0.0.1,192.168.1.2  # Replace with your machine's IP

     # Upstream DNS servers
     server=8.8.8.8
     server=8.8.4.4

     # Domain blocking
     addn-hosts=/etc/dnsmasq.d/blocklist.conf
     ```

3. **Create Blocklist File**:
   - Create a file for blocked domains:
     ```bash
     sudo nano /etc/dnsmasq.d/blocklist.conf
     ```
   - Add domains you want to block:
     ```bash
     0.0.0.0 ad.example.com
     0.0.0.0 tracker.example.com
     ```

4. **Restart `dnsmasq`** to apply changes:
   ```bash
   sudo systemctl restart dnsmasq
   ```

#### **3. Implement Domain Filtering**

1. **Automate Blocklist Updates**:
   - Write a script to fetch updated block lists:
     ```bash
     sudo nano /usr/local/bin/update-blocklist.sh
     ```
   - Example script to download and update blocklist:
     ```bash
     #!/bin/bash
     curl -sS https://example.com/blocklist.txt -o /etc/dnsmasq.d/blocklist.conf
     sudo systemctl restart dnsmasq
     ```

2. **Make the Script Executable**:
   ```bash
   sudo chmod +x /usr/local/bin/update-blocklist.sh
   ```

3. **Schedule Regular Updates with Cron**:
   - Open cron jobs:
     ```bash
     sudo crontab -e
     ```
   - Schedule the script to run daily:
     ```bash
     0 2 * * * /usr/local/bin/update-blocklist.sh
     ```

#### **4. Configure DNS on Your Network**

1. **Set DNS Server on Router**:
   - Access your router settings and change the DNS server to the IP address of your computer running `dnsmasq`.

2. **Test DNS Resolution**:
   - On a device in your network, check DNS queries and ensure blocked domains are not accessible:
     ```bash
     nslookup ad.example.com
     ```

#### **5. Enhance Functionality and Monitoring**

1. **Install and Configure a Web Server (Optional)**:
   - Install `lighttpd` for a simple web interface:
     ```bash
     sudo apt-get install lighttpd
     ```
   - Configure to serve statistics or logs:
     ```bash
     sudo nano /var/www/html/index.html
     ```
   - Add simple HTML to display DNS query logs.

2. **Use `logrotate` for Log Management**:
   - Configure log rotation to manage log files and prevent disk space issues:
     ```bash
     sudo nano /etc/logrotate.d/dnsmasq
     ```
   - Example configuration:
     ```bash
     /var/log/dnsmasq.log {
         daily
         rotate 7
         compress
         missingok
         notifempty
         create 640 dnsmasq adm
         postrotate
             /etc/init.d/dnsmasq restart > /dev/null
         endscript
     }
     ```

3. **Implement Additional Security Measures**:
   - Consider using `unbound` for DNS over TLS/HTTPS to encrypt DNS queries.

### **Conclusion**

By following these steps, you can set up a DNS server and filter that provides ad-blocking, security, and content control tailored to your needs. This setup offers an effective way to manage and secure DNS traffic on a home or small business network, improving privacy and reducing unwanted content. For additional features and scalability, you can explore more advanced DNS software or integrate with other security tools.

### **FAQs**

1. **Why use a custom DNS filter?**
   - A custom DNS filter provides control over web content, improves network security, and reduces exposure to ads and trackers.

2. **Can I use this setup in a large organization?**
   - While this setup is suitable for small to medium-sized networks, larger organizations might require more robust solutions like dedicated DNS filtering appliances or services.

3. **How do I maintain the blocklist?**
   - Automate updates with scripts and cron jobs, and regularly check for new sources of blocklists to keep your filters effective.

4. **Is this setup secure?**
   - Basic DNS filtering adds a layer of security, but for enhanced protection, consider using DNS over HTTPS/TLS and integrating with broader security measures.

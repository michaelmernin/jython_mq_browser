package com.mqclient.mqbrowser;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class MqbrowserApplication {

    public static void main(String[] args) {
        SpringApplication.run(MqbrowserApplication.class, args);

    }

    @Bean(name = "clientServiceFactory")
    public ClientServiceFactory clientFactory() {
        return new ClientServiceFactory();
    }

    @Bean(name = "clientServicePython")
    public ClientService clientServicePython() throws Exception {
        return clientFactory().getObject();

    }
}
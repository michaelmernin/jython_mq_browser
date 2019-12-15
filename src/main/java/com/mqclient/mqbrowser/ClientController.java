package com.mqclient.mqbrowser;

import org.python.core.PyString;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class ClientController {

    @Autowired
    @Qualifier("clientServicePython")
    private ClientService service;

    @GetMapping("/")
    public List<PyString> readQ(){

        List<PyString> x = service.browse_messages_return_all_as_string();

        return service.browse_messages_return_all_as_string();
    }
}

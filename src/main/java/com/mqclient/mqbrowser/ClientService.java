package com.mqclient.mqbrowser;

import org.python.core.PyString;

import java.util.List;

public interface ClientService {
    String search_for_msgs();

    List<PyString> browse_messages_return_all_as_string();
}

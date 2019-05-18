/* File is: ElliottServer.java Clark Elliott 2019

Simplest Multithreaded echo server. Works with ElliottClient.java
Start each program in its own JVM.

Windows Bat:
start java ElliottServer
start java ElliottClient

----------------------------------------------------------------------*/

import java.io.*;  // Get the Input Output libraries
import java.net.*; // Get the Java networking libraries

class Worker extends Thread {    // Class definition
  Socket sock;                   // Class member, socket, local to Worker.
  Worker (Socket s) {sock = s;}  // Constructor, assign arg s to local sock

  public void run(){
    PrintStream out = null; // Get I/O streams from the socket
    BufferedReader in = null;
    try {
      out = new PrintStream(sock.getOutputStream());
      in = new BufferedReader
	(new InputStreamReader(sock.getInputStream()));
      String ClientString;
      ClientString = in.readLine ();
      System.out.println("Client sent: " + ClientString);
      out.println("You sent: " + ClientString);
      sock.close(); // close this connection, but not the server;
    } catch (IOException ioe) {System.out.println(ioe);}
  }
}

public class ElliottServer {
  
  public static boolean controlSwitch = true;
  
  public static void main(String a[]) throws IOException {
    int q_len = 6; // Not interesting; number of requests for OpSys to queue
    int port = 2525;
    Socket sock;
    
    ServerSocket servsock = new ServerSocket(port, q_len);
    System.out.println("Clark Elliott's simple echo server starting at 2525.\n");
    while (controlSwitch) {
      sock = servsock.accept(); // Wait for the next client connection
      new Worker (sock).start(); // Spawn a thread to handle it
    }
  }
}


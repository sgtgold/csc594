/* File is: ElliottServer.java Clark Elliott 2019

Simplest Multithreaded echo server. Works with ElliottClient.java
Start each program in its own JVM.

Windows Bat:
start java ElliottServer
start java ElliottClient

----------------------------------------------------------------------*/

import java.io.*;  // Get the Input Output libraries
import java.net.*; // Get the Java networking libraries

public class ElliottClient{
  public static void main (String args[]) {
    String serverName;
    if (args.length < 1) serverName = "localhost";
    else serverName = args[0];
    
    System.out.println("Clark Elliott's Simple Socket Client.\n");
    System.out.println("Using server: " + serverName + ", Port: 2525");
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    try {
      String name;
      do {
	System.out.print
	  ("Enter a string and the server will echo it back to you. Use [quit] to stop client: ");
	System.out.flush ();
	name = in.readLine ();
	if (name.indexOf("quit") < 0)
	  getReply(name, serverName);
      } while (name.indexOf("quit") < 0);
      System.out.println ("Cancelled by user request.");
    } catch (IOException x) {x.printStackTrace ();}
  }
  
  static void getReply (String ToServerString, String serverName){
    Socket sock;
    BufferedReader fromServer;
    PrintStream toServer;
    String textFromServer;
    
    try{
      /* Open our connection to server port, choose your own port number.. */
      sock = new Socket(serverName, 2525);
      
      // Create filter I/O streams for the socket:
      fromServer = 
	new  BufferedReader(new InputStreamReader(sock.getInputStream()));
      toServer   = new PrintStream(sock.getOutputStream());
      
      // Send string to the server:
      toServer.println(ToServerString); toServer.flush(); 
      
      // Read up to 3 lines of response from the server, and block while synchronously waiting:
      for (int i = 1; i <=3; i++){
	textFromServer = fromServer.readLine();
	if (textFromServer != null) System.out.println(textFromServer);
      }
      
      sock.close();
    } catch (IOException x) {
      System.out.println ("Socket error.");
      x.printStackTrace ();
    }
  }
}

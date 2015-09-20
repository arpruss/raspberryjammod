package mobi.omegacentauri.raspberryjammod;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.Serializable;
import java.io.Writer;
import java.net.InetSocketAddress;
import java.net.UnknownHostException;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import org.java_websocket.WebSocket;
import org.java_websocket.WebSocketImpl;
import org.java_websocket.framing.Framedata;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;
import org.omg.CORBA.Any;
import org.omg.CORBA.DataOutputStream;
import org.omg.CORBA.TypeCode;

public class WSServer extends WebSocketServer {
	Map<WebSocket, APIHandler> handlers;
	boolean controlServer;
	private MCEventHandler eventHandler;
	
	public WSServer( MCEventHandler eventHandler, int port, boolean clientSide ) throws UnknownHostException {
		super( new InetSocketAddress( port ) );
		controlServer = ! clientSide;
		this.eventHandler = eventHandler;
		handlers = new HashMap<WebSocket,APIHandler>();
	}

	@Override
	public void onOpen( final WebSocket conn, ClientHandshake handshake ) {
		Writer writer = new Writer() {
			@Override
			public void close() throws IOException {
			}

			@Override
			public void flush() throws IOException {
			}

			@Override
			public void write(char[] data, int start, int len)
					throws IOException {
				conn.send(new String(data, start, len));
			}
		};
		PrintWriter pw = new PrintWriter(writer);
		try {
			APIHandler apiHandler = controlServer ? new APIHandler(eventHandler, pw) : new APIHandlerClientOnly(eventHandler, pw);
			handlers.put(conn, apiHandler);
		} catch (IOException e) {
		}
	}

	@Override
	public void onClose( WebSocket conn, int code, String reason, boolean remote ) {
		APIHandler apiHandler = handlers.get(conn);
		if (apiHandler != null) {
			apiHandler.writer.close();
			handlers.remove(conn);
		}
	}

	@Override
	public void onMessage( WebSocket conn, String message ) {
		APIHandler apiHandler = handlers.get(conn);
		if (apiHandler != null) {
			apiHandler.process(message);
		}
	}


	@Override
	public void onError( WebSocket conn, Exception ex ) {
	}
}

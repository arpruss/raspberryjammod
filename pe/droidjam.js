// droidjam.js (c) 2015 by Alexander R. Pruss
//
// Based on : Simple finger server
// Copyright (c) 2009 by James K. Lawless (jimbo@radiks.net http://www.radiks.net/~jimbo)
//
// License: MIT / X11
//
// Permission is hereby granted, free of charge, to any person
// obtaining a copy of this software and associated documentation
// files (the "Software"), to deal in the Software without
// restriction, including without limitation the rights to use,
// copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following
// conditions:
//
// The above copyright notice and this permission notice shall be
// included in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
// OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
// HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
// WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
// OTHER DEALINGS IN THE SOFTWARE.

//importPackage(java.net);
//importPackage(java.io);

var serv;
var socket;
var reader;
var writer;
var thread;
var running;

var blockQueue = [];

function newLevel() {
   print("new Level");
   running = true;
   thread = new java.lang.Thread(runServer);
   thread.start();
}

function runServer() {
   try {
       serv=new java.net.ServerSocket(4711,1);
   }
   catch(e) {
       print("Error "+e);
       return;
   }
   while(running) {
      reader = undefined;
      writer = undefined;
      socket = undefined;

      try {
//          print("awaiting connection");
          if (!running)
              break;
          socket=serv.accept();
          reader=new java.io.BufferedReader(
             new java.io.InputStreamReader(
                socket.getInputStream()));
          writer=new java.io.PrintWriter(socket.getOutputStream(),true);
          Level.setTime(0);

          while(running) {
             var str = reader.readLine();
             if (undefined == str)
                break;
//             android.util.Log.v("droidjam", str);
             handleCommand(str);
             //writer.println("Received message "+str);
          }
      }
      catch(e) {
         if (running)
             print("Error "+e);
      }
      print("closing connection");
      android.util.Log.v("droidjam", "closing connection");
      try {
           reader.close();
      } catch(e) {}
      reader = undefined;
      try {
          writer.close();
      } catch(e) {}
      writer = undefined;
      try {
          socket.close();
      } catch(e) {}
      socket = undefined;
      android.util.Log.v("droidjam", "closed connection");
   }
   try {
      serv.close();
      android.util.Log.v("droidjam", "closed socket");
   } catch(e) {}
}

function leaveGame() {
   android.util.Log.v("droidjam", "leaveGame()");
   print("leaveGame()");
   running = false;
   try {
       reader.close();
   }
   catch(e) {}
   try {
       writer.close();
   }
   catch(e) {}
   try {
       socket.close();
   }
   catch(e) {}
   try {
       serv.close();
       print("closed server");
   }
   catch(e) {}
}

function handleCommand(cmd) {
   cmd = cmd.trim();
   var n = cmd.indexOf("(");
   if (n==-1 || cmd.slice(-1) != ")") {
       err("Cannot parse");
       return;
   }
   var m = cmd.substring(0,n);
   var argList = cmd.substring(n+1,cmd.length()-1);
   var args = argList.split(",");
   if (m == "world.setBlock") {
       setBlock(args);
   }
   else if (m == "world.setBlocks") {
       setBlocks(args);
   }
   else if (m == "player.getPos") {
       writer.println(""+Player.getX()+","+Player.getY()+","+Player.getZ());
   }
   else if (m == "world.getPlayerId") {
       writer.println(""+Player.getEntity());
   }
   else if (m == "player.setPos") {
       Entity.setPosition(Player.getEntity(),args[0],args[1],args[2]);
   }
   else if (m == "player.getPitch") {
       writer.println(""+getPitch(Player.getEntity()));
   }
   else if (m == "player.getRotation") {
       writer.println(""+getYaw(Player.getEntity()));
   }
   else if (m == "chat.post") {
       clientMessage(argList);
   }
   else {
       err("Unknown command");
    }
}

var busy = 0;

function pushBlockQueue(x,y,z,id,meta) {
    var entry = [x,y,z,id,meta];
    while(busy){
        java.lang.Thread.sleep(77);
    }
    busy++;
    blockQueue.push(entry);
    busy--;
}

function setBlock(args) {
    pushBlockQueue(parseInt(args[0]),parseInt(args[1]),parseInt(args[2]),parseInt(args[3]),parseInt(args[4]));
}

function modTick() {
    if (busy) {
        return;
    }
    busy++;
    var count = blockQueue.length;
    if (count > 0) {
        if (count > 100) {
            count = 100;
        }
        var grabbed = blockQueue.slice(0,count);
        blockQueue = blockQueue.slice(count);
        for (i = 0 ; i < count ; i++) {
            var e = grabbed[i];
            Level.setTile(e[0], e[1], e[2], e[3], e[4]);
        }
    }
    busy--;
}

function setBlocks(args) {
   var x0 = parseInt(args[0]);
   var y0 = parseInt(args[1]);
   var z0 = parseInt(args[2]);
   var x1 = parseInt(args[3]);
   var y1 = parseInt(args[4]);
   var z1 = parseInt(args[5]);
   var id = parseInt(args[6]);
   var meta = parseInt(args[7]);
   var startx = x0 < x1 ? x0 : x1;
   var starty = y0 < y1 ? y0 : y1;
   var startz = z0 < z1 ? z0 : z1;
   var endx = x0 > x1 ? x0 : x1;
   var endy = y0 > y1 ? y0 : y1;
   var endz = z0 > z1 ? z0 : z1;
   for (x = startx ; x <= endx ; x++) {
       for (y = starty ; y <= endy ; y++) {
           for (z = startz ; z <= endz ; z++) {
                //Level.setTile(x, y, z, args[6], args[7]);
                pushBlockQueue(x,y,z,id,meta);
           }
       }
   }
}

function err(msg) {
   writer.println("ERR "+msg);
   print("ERR "+msg);
}

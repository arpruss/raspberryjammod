// droidjam.js (c) 2015 by Alexander R. Pruss
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


// Done:
// chat.post, world.setBlock, world.setBlocks, world.getBlock, world.getBlockWithData,
// player.setTile, player.setPos, player.setRotation, player.setPitch, player.getPitch,
// player.getRotation, world.getPlayerIds, entity.setPos, entity.setTile, entity.getPos,
// entity.getTile, world.spawnEntity, world.removeEntity,

// To do:
// world.getHeight,
// world.setting, player.setDirection, player.getDirection, events.block.hits, events.chat.posts,
// events.clear, events.setting, camera.setFollow, camera.setNormal, camera.getEntityId

var BLOCKS_PER_TICK = 20;

var serverSocket;
var socket;
var reader;
var writer;
var thread;
var running;

var blockQueue = [];
var playerId;
//var noAIs = [];
var ENTITIES = {
    "PrimedTnt":65,
    "FallingSand":66,
    "Arrow":80,
    "Snowball":81,
    "MinecartRideable":84,
    "Fireball":85,
    "Zombie":32,
    "Creeper":33,
    "Skeleton":34,
    "Spider":35,
    "PigZombie":36,
    "Slime":37,
    "Enderman":38, //untested from here
    "Silverfish":39,
    "CaveSpider":40,
    "Ghast":41,
    "LavaSlime":42,
    "Chicken":10,
    "Cow":11,
    "Pig":12,
    "Sheep":13,
    "Wolf":14,
    "Mooshroom":16,
    "Squid":17,
    "Bat":19
};

function newLevel() {
   running = 1;
   thread = new java.lang.Thread(runServer);
   thread.start();
   playerId = Player.getEntity();
}

function runServer() {
   try {
       serverSocket=new java.net.ServerSocket(4711,1);
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
          if (!running)
              break;
          socket=serverSocket.accept();
          reader=new java.io.BufferedReader(new java.io.InputStreamReader(socket.getInputStream()));
          writer=new java.io.PrintWriter(socket.getOutputStream(),true);
//          Level.setTime(0); // only for debug

          while(running) {
             var str = reader.readLine();
             if (undefined == str)
                break;
             handleCommand(str);
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
      serverSocket.close();
      android.util.Log.v("droidjam", "closed socket");
   } catch(e) {}
}

function leaveGame() {
   android.util.Log.v("droidjam", "leaveGame()");
   print("leaveGame()");
   running = 0;
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
       serverSocket.close();
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
   else if (m == "player.getTile") {
       writer.println(""+Math.floor(Player.getX())+","+Math.floor(Player.getY())+","+Math.floor(Player.getZ()));
   }
   else if (m == "entity.getPos") {
       writer.println(Entity.getX(args[0])+","+Entity.getY(args[0])+","+Entity.getZ(args[0]));
   }
   else if (m == "entity.getTile") {
       writer.println(Math.floor(Entity.getX(args[0]))+","+Math.floor(Entity.getY(args[0]))+","+Math.floor(Entity.getZ(args[0])));
   }
   else if (m == "world.getPlayerId" || m == "world.getPlayerIds") {
       writer.println(""+playerId);
   }
   else if (m == "entity.setPos" || m == "entity.setTile") {
       Entity.setPosition(args[0],args[1],args[2],args[3]);
       Entity.setVelX(args[0],0);
       Entity.setVelY(args[0],0);
       Entity.setVelZ(args[0],0);
   }
   else if (m == "player.setPos" || m == "player.setTile") {
       Entity.setPosition(playerId,args[0],args[1],args[2]);
       Entity.setVelX(playerId,0);
       Entity.setVelY(playerId,0);
       Entity.setVelZ(playerId,0);
   }
   else if (m == "player.getPitch") {
       writer.println(""+getPitch(playerId));
   }
   else if (m == "player.getRotation") {
       writer.println(""+getYaw(playerId));
   }
   else if (m == "player.setPitch") {
       setRot(playerId, getYaw(playerId), args[0]);
   }
   else if (m == "player.setRotation") {
       setRot(playerId, args[0], getPitch(playerId));
   }
   else if (m == "entity.setPitch") {
       setRot(args[0], getYaw(args[0]), args[1]);
   }
   else if (m == "entity.setRotation") {
       setRot(args[0], args[1], getPitch(args[0]));
   }
   else if (m == "world.getBlock") {
       writer.println(""+Level.getTile(args[0], args[1], args[2]));
   }
   else if (m == "world.getBlockWithData") {
       writer.println(""+Level.getTile(args[0], args[1], args[2])+","+Level.getData(args[0], args[1], args[2]));
   }
   else if (m == "chat.post") {
       clientMessage(argList);
   }
   else if (m == "world.spawnEntity") {
       var id;
       if (args[0] == "Cow") {
           id = spawnCow(args[1], args[2], args[3]);
       }
       else if (args[0] == "Chicken") {
           id = spawnChicken(args[1], args[2], args[3]);
       }
       else if (! isNaN(args[0])) {
           id = Level.spawnMob(args[1], args[2], args[3], args[0]);
       }
       else if (args[0] in ENTITIES) {
           id = Level.spawnMob(args[1], args[2], args[3], ENTITIES[args[0]]);
       }
       writer.println(""+id);
//       if (args.length >= 5 && args[4]) {
//           var e = [id, args[1], args[2], args[3], 0, 0];
//           noAIs.push(e);
//           android.util.Log.v("droidjam", "closing connection");
//       }
   }
   else if (m == "entity.rideAnimal") { // unofficial
       Entity.rideAnimal(args[0], args[1]);
   }
   else if (m == "world.removeEntity") {
       Entity.remove(args[0]);
   }
   else {
       err("Unknown command");
    }
}

var busy = 0;

function _pushBlockQueue(x,y,z,id,meta) {
    var entry = [x,y,z,id,meta];
    blockQueue.push(entry);
}

pushBlockQueue = new Packages.org.mozilla.javascript.Synchronizer(_pushBlockQueue);

function setBlock(args) {
    pushBlockQueue(parseInt(args[0]),parseInt(args[1]),parseInt(args[2]),parseInt(args[3]),parseInt(args[4]));
}

function _grab() {
    var count = blockQueue.length;
    if (count == 0)
        return [];
    if (count > BLOCKS_PER_TICK) {
        count = BLOCKS_PER_TICK;
    }
    var grabbed = blockQueue.slice(0,count);
    blockQueue = blockQueue.slice(count);
    return grabbed;
}

grab = new Packages.org.mozilla.javascript.Synchronizer(_grab);

function modTick() {
//    for (i = 0 ; i < noAIs.length ; i++) {
//        e = noAIs[i];
//        Entity.setPosition(e[0],e[1],e[2],e[3]);
//        setRot(e[0], e[4], e[5]);
//    }
    if (busy) {
        // try again next tick
        return;
    }
    busy++;
    var grabbed = grab();
    for (i = 0 ; i < grabbed.length ; i++) {
        var e = grabbed[i];
        Level.setTile(e[0], e[1], e[2], e[3], e[4]);
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
   for (z = startz ; z <= endz ; z++) {
       for (y = starty ; y <= endy ; y++) {
           for (x = startx ; x <= endx ; x++) {
                pushBlockQueue(x,y,z,id,meta);
           }
       }
   }
}

function err(msg) {
   writer.println("ERR "+msg);
   android.util.Log.e("droidjam", "error "+msg);
}

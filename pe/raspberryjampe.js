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
// entity.getTile, world.spawnEntity, world.removeEntity, world.getHeight, events.block.hits,
// events.clear, events.setting, events.chat.posts, entity.getPitch, entity.getRotation,
// player.setDirection, player.getDirection, 

// Not done:
// world.setting,
// camera.setFollow, camera.setNormal, camera.getEntityId

// Divergences:
// The positions are NOT relative to the spawn point.
// Chat posts all return the player's ID as the callback function doesn't specify the speaker.
// world.spawnEntity() does not support NBT tag.


// 20 is reliable
// 80 seems OK
var BLOCKS_PER_TICK = 100;
var PORT = 4711;
var EVENTS_MAX = 512;
var PLAYER_HEIGHT = 1.61999988;
var TOO_SMALL = 1e-9;

var serverSocket;
var socket;
var reader;
var writer;
var thread;
var running;

var hitRestrictedToSword = 1;
var blockQueue = [];
var hitData = [];
var chatData = [];
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

function newLevel(hasLevel) {
   android.util.Log.v("droidjam", "newLevel "+hasLevel);
   running = 1;
   thread = new java.lang.Thread(runServer);
   thread.start();
   playerId = Player.getEntity();
}

function sync(f) {
   return new Packages.org.mozilla.javascript.Synchronizer(f);
}

function _addHit(data) {
   hitData.push(data);
   while(hitData.length > EVENTS_MAX) {
       hitData.shift();
   }
}

function _addChat(data) {
   chatData.push(data);
   while(chatData.length > EVENTS_MAX) {
       chatData.shift();
   }
}

function _getAndClearHits() {
    var out = "";
    for (i = 0; i < hitData.length ; i++) {
        if (i > 0) {
            out += "|";
        }
        out += hitData[i];
    }
    hitData = [];
    return out;
}

function _getAndClearChats() {
    var out = "";
    for (i = 0; i < chatData.length ; i++) {
        if (i > 0) {
            out += "|";
        }
        out += chatData[i];
    }
    chatData = [];
    return out;
}

function _clearHits() {
    hitData = [];
}

function _clearChats() {
    chatData = [];
}

function _restrictToSword(x) {
    hitRestrictedToSword = x;
}

eventSync = {
          addHit: sync(_addHit),
          addChat: sync(_addChat),
          getAndClearHits: sync(_getAndClearHits),
          getAndClearChats: sync(_getAndClearChats),
          clearHits: sync(_clearHits),
          clearChats: sync(_clearChats),
          restrictToSword: _restrictToSword };

function useItem(x,y,z,itemId,blockId,side) {
   if (! hitRestrictedToSword || itemId == 267 || itemId == 268 || itemId == 272 || itemId == 276 || itemId == 283) {
       eventSync.addHit([x,y,z,side,playerId]);
   }
}

function chatHook(message) {
   data = [playerId, message.replace(/\|/g, '&#124;')];
   eventSync.addChat(data);
}

function posDesc(desc,x) {
    desc = desc.replace(/[A-Za-z]/, '~');
    if (desc.charAt(0) != "~") {
        return desc;
    }
    var adj = desc.substring(1);
    if (adj.charAt(0) == "+") {
        adj = adj.substring(1);
    }
    if (isNaN(parseFloat(adj))) {
        adj = "0";
    }
    return x + parseFloat(adj);
}

// OOPS: no way to get a context, which would be needed to launch
function procCmd(cmdLine) {
    cmds = cmdLine.split(/ +/);
    if (cmds[0] == "set") {
        if (cmds.length >= 3 && cmds[1] == "time") {
            Level.setTime(cmds[2]);
        }
    }
    else if (cmds[0] == "tp" && cmds.length >= 4) {
        x = Player.getX();
        y = Player.getY()-PLAYER_HEIGHT;
        z = Player.getZ();
        Entity.setVelX(playerId,0);
        Entity.setVelY(playerId,0);
        Entity.setVelZ(playerId,0);
        Entity.setPosition(playerId,posDesc(cmds[1],x),posDesc(cmds[2],y),posDesc(cmds[3],z));
    }
}

function closeAllButServer() {
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
}

function closeServer() {
   try {
      serverSocket.close();
      android.util.Log.v("droidjam", "closed socket");
   } catch(e) {}
}

function runServer() {
   try {
       serverSocket=new java.net.ServerSocket(PORT,1);
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
          android.util.Log.v("droidjam", "opening connection");
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
      closeAllButServer();
   }

   closeServer();
   print("Closing server");
}

function leaveGame() {
   android.util.Log.v("droidjam", "leaveGame()");
   running = 0;
   closeAllButServer();
   closeServer();
}

function entitySetDirection(id, x, y, z) {
   if (x * x + y * y + z * z >= TOO_SMALL * TOO_SMALL) {

       var xz = Math.sqrt(x * x + z * z);
       var yaw;
       if (xz >= TOO_SMALL) {
           yaw = Math.atan2(-x, z) * 180 / Math.PI;
       }
       else {
           yaw = getYaw(id);
       }

       var pitch = Math.atan2(-y, xz) * 180 / Math.PI;

       setRot(id, yaw, pitch);
   }
}

function entityGetDirection(id) {
   var pitch = getPitch(id) * Math.PI / 180.;
   var yaw = getYaw(id) * Math.PI / 180.;
   var x = Math.cos(-pitch) * Math.sin(-yaw);
   var z = Math.cos(-pitch) * Math.cos(-yaw);
   var y = Math.sin(-pitch);
   writer.println(""+x+","+y+","+z);
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
       writer.println(""+Player.getX()+","+(Player.getY()-PLAYER_HEIGHT)+","+Player.getZ());
   }
   else if (m == "player.getTile") {
       writer.println(""+Math.floor(Player.getX())+","+Math.round(Player.getY()-PLAYER_HEIGHT)+","+Math.floor(Player.getZ()));
   }
   else if (m == "entity.getPos") {
       y = Entity.getY(args[0]);
       if (args[0] == playerId) {
           y -= PLAYER_HEIGHT;
       }
       writer.println(Entity.getX(args[0])+","+y+","+Entity.getZ(args[0]));
   }
   else if (m == "entity.getTile") {
       y = Entity.getY(args[0]);
       if (args[0] == playerId) {
           y -= PLAYER_HEIGHT;
       }
       writer.println(Math.floor(Entity.getX(args[0]))+","+Math.round(y)+","+Math.floor(Entity.getZ(args[0])));
   }
   else if (m == "world.getPlayerId" || m == "world.getPlayerIds") {
       writer.println(""+playerId);
   }
   else if (m == "entity.setPos" || m == "entity.setTile") {
       var y;
       if (args[0] == playerId) {
           y = PLAYER_HEIGHT+parseFloat(args[2]);
       }
       else {
           y = args[2];
       }
       Entity.setVelX(args[0],0);
       Entity.setVelY(args[0],0);
       Entity.setVelZ(args[0],0);
       Entity.setPosition(args[0],args[1],y,args[3]);
   }
   else if (m == "player.setPos" || m == "player.setTile") {
       Entity.setVelX(playerId,0);
       Entity.setVelY(playerId,0);
       Entity.setVelZ(playerId,0);
       Entity.setPosition(playerId,args[0],PLAYER_HEIGHT+parseFloat(args[1]),args[2]);
   }
   else if (m == "player.getPitch") {
       writer.println(""+getPitch(playerId));
   }
   else if (m == "player.getRotation") {
       writer.println(""+getYaw(playerId));
   }
   else if (m == "entity.getPitch") {
       writer.println(""+getPitch(args[0]));
   }
   else if (m == "entity.getRotation") {
       writer.println(""+getYaw(args[0]));
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
   else if (m == "entity.setDirection") {
       entitySetDirection(args[0], args[1], args[2], args[3]);
   }
   else if (m == "player.setDirection") {
       entitySetDirection(playerId, args[0], args[1], args[2]);
   }
   else if (m == "entity.getDirection") {
       entityGetDirection(args[0]);
   }
   else if (m == "player.getDirection") {
       entityGetDirection(playerId);
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
   else if (m == "events.block.hits") {
       writer.println(eventSync.getAndClearHits());
   }
   else if (m == "events.chat.posts") {
       writer.println(eventSync.getAndClearChats());
   }
   else if (m == "events.clear") {
       eventSync.clearHits();
       eventSync.clearChats();
   }
   else if (m == "events.setting") {
       if(args[0] == "restrict_to_sword") {
            eventSync.restrictToSword(parseInt(args[1]));
       }
   }
   else if (m == "world.getHeight") {
       var x = parseInt(args[0]);
       var z = parseInt(args[2]);
       var y;
       for (y = 127 ; y > 0 ; y--) {
           if (Level.getTile(x,y,z)) {
               break;
           }
       }
       writer.println(""+y);
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
    pushBlockQueue(parseInt(Math.round(args[0])),
       parseInt(Math.round(args[1])),parseInt(Math.round(args[2])),
       parseInt(Math.round(args[3])),parseInt(Math.round(args[4])));
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
   var x0 = parseInt(Math.round(args[0]));
   var y0 = parseInt(Math.round(args[1]));
   var z0 = parseInt(Math.round(args[2]));
   var x1 = parseInt(Math.round(args[3]));
   var y1 = parseInt(Math.round(args[4]));
   var z1 = parseInt(Math.round(args[5]));
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

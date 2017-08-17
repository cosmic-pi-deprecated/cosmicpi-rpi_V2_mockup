window.Settings = Vue.component('settings', {
    template: `
    <div class="component-content">

		  <form class="form-horizontal">
          <h3>{{ $t('Wifi Settings') }}</h3>
          <hr />

          <div class="form-group">
            <label class="control-label col-sm-2" for="email">{{ $t('SSID') }}:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" ref="ssid" v-bind:placeholder="$t('Enter SSID')">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="pwd">{{ $t('Password') }}:</label>
            <div class="col-sm-10">
              <input type="password" class="form-control" ref="password" id="pwd" v-bind:placeholder="$t('Enter password')">
            </div>
          </div>
          <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
              <button type="submit" class="btn btn-primary" v-on:click.prevent="onConnect()">{{ $t('Connect') }}</button>
            </div>
          </div>
        </form>
    </div>
  `,
    methods: {
        onConnect() {
            events.emit('wifiSetting', {
                ssid: this.$refs.ssid.value,
                password: this.$refs.password.value
            });
        }
    }
});

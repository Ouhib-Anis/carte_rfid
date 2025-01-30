odoo.define('altex.rfid_reader', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var core = require('web.core');
    var _t = core._t;

    FormController.include({
        custom_events: _.extend({}, FormController.prototype.custom_events, {
            rfid_scanned: '_onRFIDScanned',
        }),

        _onRFIDScanned: function (event) {
            var self = this;
            var rfid_id = event.data.rfid_id;
            if (rfid_id) {
                this.model.setValue(this.handle, 'rfid_id', rfid_id);
            }
        },

        _start: function () {
            var self = this;
            this._super.apply(this, arguments);
            this.$el.on('rfid-scanned', function (e, rfid_id) {
                self.trigger_up('rfid_scanned', { rfid_id: rfid_id });
            });

            document.addEventListener('keydown', function (e) {
                // Assuming the RFID reader sends the ID as a sequence of key presses
                if (e.key === 'Enter') {
                    var rfidInput = document.getElementById('rfid_input');
                    if (rfidInput) {
                        self.$el.trigger('rfid-scanned', rfidInput.value);
                        rfidInput.value = '';  // Clear the input field
                    }
                }
            });
        },
    });
});
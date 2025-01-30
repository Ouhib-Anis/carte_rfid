odoo.define('altex.rfid_confirmation', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var NotificationManager = require('web.notification').NotificationManager;
    var _t = core._t;

    FormController.include({
        _saveRecord: function () {
            var self = this;

            // Show confirmation dialog
            Dialog.confirm(self, _t("Vous êtes sûr de créer une carte ?"), {
                confirm_callback: function () {
                    // Call the original _saveRecord method
                    self._super.apply(self, arguments).then(function () {
                        // Show success notification
                        self.do_notify(_t("Succès"), _t("La carte a été créée avec succès."));
                    });
                },
            });
        },
    });
});
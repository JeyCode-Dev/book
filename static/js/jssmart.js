/*!
 * jQuery Smart Cart v3.0.1
 * The smart interactive jQuery Shopping Cart plugin with PayPal payment support
 * http://www.techlaboratory.net/smartcart
 *
 * Created by Dipu Raj
 * http://dipuraj.me
 *
 * Licensed under the terms of the MIT License
 * https://github.com/techlab/SmartCart/blob/master/LICENSE
 */
! function(t, e, a, i) {
    "use strict";

    function s(e, a) {
        this.options = t.extend(!0, {}, r, a), this.cart = [], this.cart_element = t(e), this.init()
    }
    var r = {
        cart: [],
        resultName: "cart_list",
        theme: "default",
        combineProducts: !0,
        highlightEffect: !0,
        cartItemTemplate: '<img class="img-responsive pull-left" src="{product_image}" /><h4 class="list-group-item-heading"><div class="dropdown"><span class="dropbtn">{product_name}</span></div></h4><p class="list-group-item-text">{product_desc}</p>',
        cartItemQtyTemplate: "{display_price} × {display_quantity} = {display_amount}",
        productContainerSelector: ".sc-product-item",
        productElementSelector: "*",
        addCartSelector: ".sc-add-to-cart",
        paramSettings: {
            productPrice: "product_price",
            productPrice2: "product_price_2",
            productQuantity: "product_quantity",
            productName: "product_name",
            productId: "product_id"
        },
        lang: {
            cartTitle: "Détail Commande",
            checkout: "Valider",
            clear: "Effacer",
            subtotal: "Total Gén.:",
            cartRemove: "×",
            cartEmpty: "Commande vide!<br />Choisir un article"
        },
        submitSettings: {
            submitType: "form",
            ajaxURL: "",
            ajaxSettings: {}
        },
        currencySettings: {
            locales: "fr-FR",
            currencyOptions: {
                style: "currency",
                currency: "USD",
                currencyDisplay: "symbol"
            }
        },
        toolbarSettings: {
            showToolbar: !0,
            showCheckoutButton: !0,
            showClearButton: !0,
            showCartSummary: !0,
            checkoutButtonStyle: "default",
            checkoutButtonImage: "",
            toolbarExtraButtons: []
        },
        debug: !1
    };
    t.extend(s.prototype, {
        init: function() {
            this._setElements(), this._setToolbar(), this._setEvents();
            var e = this;
            t(this.options.cart).each(function(t, a) {
                a = e._addToCart(a)
            }), this._hasCartChange()
        },
        _setElements: function() {
            var e = t('<input type="hidden" name="' + this.options.resultName + '" id="' + this.options.resultName + '" />');
            this.cart_element.append(e), this.cart_element.addClass("card border-success sc-cart sc-theme-" + this.options.theme), this.cart_element.append('<div class="card-header bg-secondary text-white sc-cart-heading">' + this.options.lang.cartTitle + ' <span class="sc-cart-count badge badge-pill badge-dark">0</span></div>'), this.cart_element.append('<div style="overflow: auto;max-height: 300px" class="list-group sc-cart-item-list"></div>')
        },
        _setToolbar: function() {
            if (this.options.toolbarSettings.showToolbar !== !0) return !1;
            var e = t('<div></div>').addClass("card-footer sc-toolbar"),
                a = t('<div class="sc-cart-toolbar">'),
                i = t('<div class="sc-cart-summary">');
                //e.append('<p><div class="text-center bt-1 border-light p-2"><div class="form-check form-check-inline"><input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2"  value="TA" checked><label class="form-check-label" for="flexRadioDefault2">EMPORTER</label></div></p><div class="form-check form-check-inline"><input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1" value="SP" ><label class="form-check-label" for="flexRadioDefault1">SUR PLACE</label></div><div class="form-check form-check-inline"><input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault3" value="LIV"><label class="form-check-label" for="flexRadioDefault3">LIVRER</label></div></div></p>')
            if (this.options.toolbarSettings.showCheckoutButton) {
                var s = "";
                switch (this.options.toolbarSettings.checkoutButtonStyle) {
                    case "paypal":
                        s = '<button class="sc-button-checkout-paypal sc-cart-checkout" type="submit"><img src="https://www.paypalobjects.com/webstatic/en_US/i/buttons/checkout-logo-medium.png" alt="Check out with PayPal" /></button>';
                        break;
                    case "image":
                        s = '<button class="sc-button-checkout-paypal sc-cart-checkout" type="submit"><img src="' + this.options.toolbarSettings.checkoutButtonImage + '" alt="Check out" /></button>';
                        break;
                    default:
                        s = '<button class="btn btn-info sc-cart-checkout" type="button">' + this.options.lang.checkout + "</button> "
                }
                a.append(s)
            }
            if (this.options.toolbarSettings.showClearButton) {
                var r = t('<button class="btn btn-danger sc-cart-clear" type="button">').text(this.options.lang.clear);
                a.append(r)
            }
            if (this.options.toolbarSettings.toolbarExtraButtons && this.options.toolbarSettings.toolbarExtraButtons.length > 0 && a.append(this.options.toolbarSettings.toolbarExtraButtons), this.options.toolbarSettings.showCartSummary) {
                var n = t('<div class="sc-cart-summary-subtotal">');
                n.append(this.options.lang.subtotal).append(' <span class="sc-cart-subtotal">0</span>'), i.append(n)
            }
            e.append(i), e.append(a), this.cart_element.append(e)
        },
        _setEvents: function() {
            var e = this;
            t(this.options.addCartSelector).on("click", function(a) {
                a.preventDefault();
                var i = e._getProductDetails(t(this));
                i = e._addToCart(i), t(this).parents(e.options.productContainerSelector).addClass("sc-added-item").attr("data-product-unique-key", i.unique_key)
            }), t(this.cart_element).on("click", ".sc-cart-remove", function(a) {
                a.preventDefault(), t(this).parents(".sc-cart-item").fadeOut("normal", function() {
                    e._removeFromCart(t(this).data("unique-key")), t(this).remove(), e._hasCartChange()
                })
            }),t(this.cart_element).on("dblclick", ".list-group-item-headingg", function(a) {
                a.preventDefault();

                var code=t(this).parents(".sc-cart-item").data("unique-key");

                t.each(e.cart, function(t, r) {
                    if (r.unique_key === code) return (e.cart[t][e.options.paramSettings.productPrice] = "5000"), e._updatePriceCartItem(e.cart[t]), this._triggerEvent("priceUpdated", [e.cart[t], "5000"]), !1
                });
            }), t(this.cart_element).on("change", ".sc-cart-item-qty", function(a) {
                a.preventDefault(), e._updateCartQuantity(t(this).parents(".sc-cart-item").data("unique-key"), t(this).val())
            }), t(this.cart_element).on("click", ".sc-cart-checkout", function(a) {
                if (t(this).hasClass("disabled")) return !1;
                a.preventDefault(), e._submitCart()
            }), t(this.cart_element).on("click", ".sc-cart-clear", function(a) {
                if (t(this).hasClass("disabled")) return !1;
                a.preventDefault(), t(".sc-cart-item-list > .sc-cart-item", this.cart_element).fadeOut("normal", function() {
                    t(this).remove(), e._clearCart(), e._hasCartChange()
                })
            })
        },
        _getProductDetails: function(e) {
            var a = this,
                i = {};
            return e.parents(this.options.productContainerSelector).find(this.options.productElementSelector).each(function() {
                if (t(this).is("[name]") === !0 || void 0 !== t(this).data("name")) {
                    var e = t(this).attr("name") ? t(this).attr("name") : t(this).data("name"),
                        s = a._getContent(t(this));
                    e && s && (i[e] = s)
                }
            }), i
        },
        _addToCart: function(e) {

            var a = this;
            if (!e.hasOwnProperty(this.options.paramSettings.productPrice)) return this._logError("Price is not set for the item"), !1;
            if (e.hasOwnProperty(this.options.paramSettings.productQuantity) || (this._logMessage("Quantity not found, default to 1"), e[this.options.paramSettings.productQuantity] = 1), e.hasOwnProperty("unique_key") || (e.unique_key = this._getUniqueKey()), this.options.combineProducts) {
                var i = t.grep(this.cart, function(t, i) {

                    return a._isObjectsEqual(t, e)
                });

                if (i.length > 0) {
                    var s = this.cart.indexOf(i[0]);
                    this.cart[s][this.options.paramSettings.productQuantity] = this.cart[s][this.options.paramSettings.productQuantity] - 0 + (e[this.options.paramSettings.productQuantity] - 0), e = this.cart[s], this._triggerEvent("itemUpdated", [e])
                } else this.cart.unshift(e), this._triggerEvent("itemAdded", [e])
            } else this.cart.unshift(e), this._triggerEvent("itemAdded", [e]);
            return this._addUpdateCartItem(e), e
        },
        _removeFromCart: function(e) {
            var a = this;
            t.each(this.cart, function(i, s) {
                if (s.unique_key === e) {
                    var r = a.cart[i];
                    return a.cart.splice(i, 1), t('*[data-product-unique-key="' + e + '"]').removeClass("sc-added-item"), a._hasCartChange(), this._triggerEvent("itemRemoved", [r]), !1
                }
            })
        },
        _clearCart: function() {
            this.cart = [], this._triggerEvent("cartCleared"), this._hasCartChange()
        },
        _updateCartQuantity: function(e, a) {
            var i = this,
                s = this._getValidateNumber(a);
            t.each(this.cart, function(t, r) {
                if (r.unique_key === e) return s && (i.cart[t][i.options.paramSettings.productQuantity] = a), i._addUpdateCartItem(i.cart[t]), this._triggerEvent("quantityUpdated", [i.cart[t], a]), !1
            })
        },
        _updatePriceCartItem: function(e) {
            var a = (e[this.options.paramSettings.productQuantity] - 0) * (e[this.options.paramSettings.productPrice] - 0),
             b =(e[this.options.paramSettings.productPrice] - 0),

                i = t(".sc-cart-item-list", this.cart_element),
                s = i.find("[data-unique-key='" + e.unique_key + "']");


            if (s && s.length > 0) s.find(".sc-cart-item-qty").val(e[this.options.paramSettings.productQuantity]), s.find(".sc-cart-item-price").text(this._getMoneyFormatted(b)), s.find(".sc-cart-item-amount").text(this._getMoneyFormatted(a));
            else {
                // s = t("<div></div>").addClass("sc-cart-item list-group-item"), s.append('<button type="button" class="sc-cart-remove">' + this.options.lang.cartRemove + "</button>"), s.attr("data-unique-key", e.unique_key), s.append(this._formatTemplate(this.options.cartItemTemplate, e));
                // var r = '<div class="sc-cart-item-summary"><span class="sc-cart-item-price">' + this._getMoneyFormatted(e[this.options.paramSettings.productPrice]) + "</span>";
                // r += ' × <input type="number" min="1" max="1000" class="sc-cart-item-qty" value="' + this._getValueOrEmpty(e[this.options.paramSettings.productQuantity]) + '" />', r += ' = <span class="sc-cart-item-amount">' + this._getMoneyFormatted(a) + "</span></div>", s.append(r), i.append(s)
            }


            this.options.highlightEffect === !0 && (s.addClass("sc-highlight"), setTimeout(function() {
                s.removeClass("sc-highlight")
            }, 500)), this._hasCartChange()
        },
        _addUpdateCartItem: function(e) {
            var a = (e[this.options.paramSettings.productQuantity] - 0) * (e[this.options.paramSettings.productPrice] - 0),
                i = t(".sc-cart-item-list", this.cart_element),
                s = i.find("[data-unique-key='" + e.unique_key + "']");


            if (s && s.length > 0) s.find(".sc-cart-item-qty").val(e[this.options.paramSettings.productQuantity]), s.find(".sc-cart-item-amount").text(this._getMoneyFormatted(a));
            else {

                s = t("<div></div>").addClass("sc-cart-item list-group-item"), s.append('<button type="button" class="sc-cart-remove">' + this.options.lang.cartRemove + "</button>"), s.attr("data-unique-key", e.unique_key), s.append(this._formatTemplate(this.options.cartItemTemplate, e));
                var r = '<div class="sc-cart-item-summary"><span class="sc-cart-item-price">' + this._getMoneyFormatted(e[this.options.paramSettings.productPrice]) + "</span>";
                r += ' × <input type="number" min="1" max="1000" class="sc-cart-item-qty" value="' + this._getValueOrEmpty(e[this.options.paramSettings.productQuantity]) + '" />', r += ' = <span class="sc-cart-item-amount">' + this._getMoneyFormatted(a) + "</span></div>", s.append(r), i.prepend(s)
            }
            this.options.highlightEffect === !0 && (s.addClass("sc-highlight"), setTimeout(function() {
                s.removeClass("sc-highlight")
            }, 500)), this._hasCartChange()
        },
        _hasCartChange: function() {

            var tot=this._getCartSubtotal().replace(',','.').replace(/[^\d\.]*/g, '');
             $('#mtnpaye').val(tot);
            t(".sc-cart-count", this.cart_element).text(this.cart.length), t(".sc-cart-subtotal", this.element).text(this._getCartSubtotal()), 0 === this.cart.length ? (t(".sc-cart-item-list", this.cart_element).empty().append(t('<div class="sc-cart-empty-msg">' + this.options.lang.cartEmpty + "</div>")), t(this.options.productContainerSelector).removeClass("sc-added-item"), t(".sc-cart-checkout, .sc-cart-clear").addClass("disabled"), this._triggerEvent("cartEmpty")) : (t(".sc-cart-item-list > .sc-cart-empty-msg", this.cart_element).remove(), t(".sc-cart-checkout, .sc-cart-clear").removeClass("disabled")), t("#" + this.options.resultName, this.cart_element).val(JSON.stringify(this.cart))
        },
        _getCartSubtotal: function() {
            var e = this,
                a = 0;
            return t.each(this.cart, function(t, i) {
                e._getValidateNumber(i[e.options.paramSettings.productPrice]) && (a += (i[e.options.paramSettings.productPrice] - 0) * (i[e.options.paramSettings.productQuantity] - 0))
            }), this._getMoneyFormatted(a)
        },
        _submitCart: function() {
            var e = this,
                a = this.cart_element.parents("form");
            if (!a) return this._logError("Form not found to submit"), !1;
            switch (this.options.submitSettings.submitType) {
                case "ajax":
                    var i = this.options.submitSettings.ajaxURL && this.options.submitSettings.ajaxURL.length > 0 ? this.options.submitSettings.ajaxURL : a.attr("action"),
                        s = t.extend(!0, {}, {
                            url: i,
                            type: "POST",
                            data: a.serialize(),
                            beforeSend: function() {
                                e.cart_element.addClass("loading")
                            },
                            error: function(t, a, i) {
                                e.cart_element.removeClass("loading"), e._logError(i)
                            },
                            success: function(t) {
                                e.cart_element.removeClass("loading"), e._triggerEvent("cartSubmitted", [e.cart]), e._clearCart()
                            }
                        }, this.options.submitSettings.ajaxSettings);
                    t.ajax(s);
                    break;
                case "paypal":
                    a.children(".sc-paypal-input").remove(), t.each(this.cart, function(t, i) {
                        var s = t + 1;
                        a.append('<input class="sc-paypal-input" name="item_number_' + s + '" value="' + e._getValueOrEmpty(i[e.options.paramSettings.productId]) + '" type="hidden">').append('<input class="sc-paypal-input" name="item_name_' + s + '" value="' + e._getValueOrEmpty(i[e.options.paramSettings.productName]) + '" type="hidden">').append('<input class="sc-paypal-input" name="amount_' + s + '" value="' + e._getValueOrEmpty(i[e.options.paramSettings.productPrice]) + '" type="hidden">').append('<input class="sc-paypal-input" name="quantity_' + s + '" value="' + e._getValueOrEmpty(i[e.options.paramSettings.productQuantity]) + '" type="hidden">')
                    }), a.submit(), this._triggerEvent("cartSubmitted", [this.cart]);
                    break;
                default:
                    a.submit(), this._triggerEvent("cartSubmitted", [this.cart])
            }
            return !0
        },
        _getContent: function(t) {
            return t.is(":checkbox, :radio") ? t.is(":checked") ? t.val() : "" : t.is("[value], select") ? t.val() : t.is("img") ? t.attr("src") : t.text()
        },
        _isObjectsEqual: function(t, e) {

            if (Object.getOwnPropertyNames(t).length !== Object.getOwnPropertyNames(e).length) return !1;

            for (var a in t)
                if ("unique_key" !== a && a !== this.options.paramSettings.productQuantity && a !== this.options.paramSettings.productPrice && (void 0 !== t[a] || void 0 !== e[a]) && t[a] !== e[a]) return !1;
            return !0
        },
        _getMoneyFormatted: function(t) {
            return t -= 0, Number(t.toFixed(2)).toLocaleString(this.options.currencySettings.locales, this.options.currencySettings.currencyOptions)
        },
        _getValueOrEmpty: function(t) {
            return t && void 0 !== t ? t : ""
        },
        _getValidateNumber: function(t) {
            return !!((t -= 0) && t > 0)
        },
        _formatTemplate: function(t, e) {
            for (var a = t.split("{"), i = "", s = 0; s < a.length; s++) {
                var r = a[s].substring(0, a[s].indexOf("}"));
                i += r.length > 0 ? a[s].replace(r + "}", this._getValueOrEmpty(e[r])) : a[s]
            }
            return i
        },
        _triggerEvent: function(e, a) {
            var i = t.Event(e);
            return this.cart_element.trigger(i, a), !i.isDefaultPrevented() && i.result
        },
        _getUniqueKey: function() {
            return (new Date).getTime()
        },
        _logMessage: function(t) {
            if (this.options.debug !== !0) return !1;
            console.log(t)
        },
        _logError: function(e) {
            if (this.options.debug !== !0) return !1;
            t.error(e)
        },
        submit: function() {
            this._submitCart()
        },
        clear: function() {
            this._clearCart()
        }
    }), t.fn.smartCart = function(e) {
        var a, i = arguments;
        return void 0 === e || "object" == typeof e ? this.each(function() {
            t.data(this, "smartCart") || t.data(this, "smartCart", new s(this, e))
        }) : "string" == typeof e && "_" !== e[0] && "init" !== e ? (a = t.data(this[0], "smartCart"), "destroy" === e && t.data(this, "smartCart", null), a instanceof s && "function" == typeof a[e] ? a[e].apply(a, Array.prototype.slice.call(i, 1)) : this) : void 0
    }
}(jQuery, window, document);


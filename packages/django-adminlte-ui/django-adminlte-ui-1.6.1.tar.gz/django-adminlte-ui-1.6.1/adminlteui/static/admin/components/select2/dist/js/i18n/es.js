/*! Select2 4.0.8 | https://github.com/select2/select2/blob/master/LICENSE.md */

!function(){if(jQuery&&jQuery.fn&&jQuery.fn.select2&&jQuery.fn.select2.amd)var e=jQuery.fn.select2.amd;e.define("select2/i18n/es",[],function(){return{errorLoading:function(){return"No se pudieron cargar los resultados"},inputTooLong:function(e){var n=e.input.length-e.maximum,r="Por favor, elimine "+n+" car";return r+=1==n?"ácter":"acteres"},inputTooShort:function(e){var n=e.minimum-e.input.length,r="Por favor, introduzca "+n+" car";return r+=1==n?"ácter":"acteres"},loadingMore:function(){return"Cargando más resultados…"},maximumSelected:function(e){var n="Sólo puede seleccionar "+e.maximum+" elemento";return 1!=e.maximum&&(n+="s"),n},noResults:function(){return"No se encontraron resultados"},searching:function(){return"Buscando…"},removeAllItems:function(){return"Eliminar todos los elementos"}}}),e.define,e.require}();
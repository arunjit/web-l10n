angular.module('localeMessages', ['pascalprecht.translate']).
constant('currentLocale', LOCALE).
config(function($translateProvider) {
  // Configure translations to use the l10n directory for JSON strings.
  $translateProvider.useStaticFilesLoader({
    prefix: '/l10n/locale_',
    suffix: '.json'
  });
  // Set en-us as the preferred and fallback language.
  $translateProvider.preferredLanguage('en-us');
  $translateProvider.fallbackLanguage('en-us');
}).
constant('availableLanguages', [
  // Available translations. Naming follows the same locale format as
  // angular-i18n.
  'de-de',
  'en-us',
  'fr-fr'
]).
run(function($translate, availableLanguages, currentLocale) {
  var hl = currentLocale;
  if (hl && availableLanguages.indexOf(hl) > -1) {
    $translate.uses(hl);
  }
});

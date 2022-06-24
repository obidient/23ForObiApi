import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

var getPathFromUrl = function getPathFromUrl(url) {
  return url.split(/[?#]/)[0];
};

var convertBreadcrumb = function convertBreadcrumb(title, toUpperCase, replaceCharacterList, transformLabel) {
  var transformedTitle = getPathFromUrl(title);

  if (transformLabel) {
    return transformLabel(transformedTitle);
  }

  if (replaceCharacterList) {
    for (var i = 0; i < replaceCharacterList.length; i++) {
      transformedTitle = transformedTitle.replaceAll(replaceCharacterList[i].from, replaceCharacterList[i].to);
    }
  }

  return toUpperCase ? decodeURI(transformedTitle).toUpperCase() : decodeURI(transformedTitle);
};

var defaultProps = {
  useDefaultStyle: false,
  rootLabel: 'Home',
  omitRootLabel: false,
  labelsToUppercase: false,
  replaceCharacterList: [{
    from: '-',
    to: ' '
  }],
  transformLabel: undefined,
  omitIndexList: undefined,
  containerStyle: null,
  containerClassName: '',
  listStyle: null,
  listClassName: '',
  inactiveItemStyle: null,
  inactiveItemClassName: '',
  activeItemStyle: null,
  activeItemClassName: ''
};

var Breadcrumbs = function Breadcrumbs(_ref) {
  var useDefaultStyle = _ref.useDefaultStyle,
      rootLabel = _ref.rootLabel,
      omitRootLabel = _ref.omitRootLabel,
      labelsToUppercase = _ref.labelsToUppercase,
      replaceCharacterList = _ref.replaceCharacterList,
      transformLabel = _ref.transformLabel,
      omitIndexList = _ref.omitIndexList,
      containerStyle = _ref.containerStyle,
      containerClassName = _ref.containerClassName,
      listStyle = _ref.listStyle,
      listClassName = _ref.listClassName,
      inactiveItemStyle = _ref.inactiveItemStyle,
      inactiveItemClassName = _ref.inactiveItemClassName,
      activeItemStyle = _ref.activeItemStyle,
      activeItemClassName = _ref.activeItemClassName;
  var router = useRouter();

  var _useState = useState(null),
      breadcrumbs = _useState[0],
      setBreadcrumbs = _useState[1];

  useEffect(function () {
    if (router) {
      var linkPath = router.asPath.split('/');
      linkPath.shift();
      var pathArray = linkPath.map(function (path, i) {
        return {
          breadcrumb: path,
          href: '/' + linkPath.slice(0, i + 1).join('/')
        };
      });
      setBreadcrumbs(pathArray);
    }
  }, [router]);

  if (!breadcrumbs) {
    return null;
  }

  return React.createElement("nav", {
    style: containerStyle,
    className: containerClassName,
    "aria-label": "breadcrumbs"
  }, React.createElement("ol", {
    style: listStyle,
    className: useDefaultStyle ? '_2jvtI' : listClassName
  }, !omitRootLabel && React.createElement("li", {
    style: inactiveItemStyle,
    className: inactiveItemClassName
  }, React.createElement(Link, {
    href: "/"
  }, React.createElement("a", null, convertBreadcrumb(rootLabel || 'Home', labelsToUppercase, replaceCharacterList, transformLabel)))), breadcrumbs.length >= 1 && breadcrumbs.map(function (breadcrumb, i) {
    if (!breadcrumb || breadcrumb.breadcrumb.length === 0 || omitIndexList && omitIndexList.find(function (value) {
      return value === i;
    })) {
      return;
    }

    return React.createElement("li", {
      key: breadcrumb.href,
      className: i === breadcrumbs.length - 1 ? activeItemClassName : inactiveItemClassName,
      style: i === breadcrumbs.length - 1 ? activeItemStyle : inactiveItemStyle
    }, React.createElement(Link, {
      href: breadcrumb.href
    }, React.createElement("a", null, convertBreadcrumb(breadcrumb.breadcrumb, labelsToUppercase, replaceCharacterList, transformLabel))));
  })));
};

Breadcrumbs.defaultProps = defaultProps;

export default Breadcrumbs;
//# sourceMappingURL=index.modern.js.map
